"""扫描异步任务"""
import socket
from celery import shared_task
from django.utils import timezone


@shared_task
def start_scan(task_id):
    """扫描入口"""
    from .models import ScanTask
    task = ScanTask.objects.get(id=task_id)
    ips = _parse_targets(task.targets)
    task.status = 'running'
    task.last_run_at = timezone.now()
    task.save(update_fields=['status', 'last_run_at'])
    for ip in ips:
        scan_probe.delay(task_id, ip, task.credential_id, task.port)


@shared_task(rate_limit='10/m', queue='scan')
def scan_probe(task_id, ip, credential_id, port):
    """扫描探测：端口探测 → 连接识别"""
    from .models import ScanTask, ScanResult
    from apps.devices.models import Credential, Device
    from engine.ssh import SSHClient
    from engine.telnet import TelnetClient
    from engine.device_detector import DeviceDetector

    # TCP 端口快速探测
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    ok = sock.connect_ex((ip, port)) == 0
    sock.close()
    if not ok:
        ScanResult.objects.create(task_id=task_id, ip=ip, port=port, status='not_found')
        return

    credential = Credential.objects.get(id=credential_id)
    raw_output = None
    login_method = None

    # 先试 SSH
    try:
        c = SSHClient()
        c.connect(ip, port, credential.username, credential.password)
        raw_output = c.execute('show version', timeout=15)
        if not raw_output:
            raw_output = c.execute('display version', timeout=15)
        login_method = 'ssh'
        c.close()
    except Exception:
        pass

    # 再试 Telnet
    if not raw_output:
        try:
            c = TelnetClient()
            c.connect(ip, port, credential.username, credential.password)
            raw_output = c.execute('show version', timeout=15)
            if not raw_output:
                raw_output = c.execute('display version', timeout=15)
            login_method = 'telnet'
            c.close()
        except Exception:
            pass

    if not raw_output:
        ScanResult.objects.create(task_id=task_id, ip=ip, port=port, status='error')
        return

    info = DeviceDetector().parse(raw_output or '')

    task = ScanTask.objects.get(id=task_id)
    scan_result = ScanResult.objects.create(
        task_id=task_id, ip=ip, port=port, status='found',
        vendor=info.get('vendor', ''), model=info.get('model', ''),
        os_version=info.get('os_version', ''), hostname=info.get('hostname', ''),
        raw_output=(raw_output or '')[:2000],
    )

    if task.auto_add:
        device, created = Device.objects.get_or_create(
            ip=ip,
            defaults={
                'name': info.get('hostname') or f'device-{ip.replace(".", "-")}',
                'vendor': info.get('vendor', ''),
                'model': info.get('model', ''),
                'os_version': info.get('os_version', ''),
                'hostname': info.get('hostname', ''),
                'serial_number': info.get('serial_number', ''),
                'login_method': login_method,
                'credential': task.credential,
                'port': port,
                'status': 'online',
                'last_seen_at': timezone.now(),
            }
        )
        scan_result.device = device
        scan_result.save(update_fields=['device'])


def _parse_targets(targets):
    """解析 IP 范围和列表"""
    ips = []
    for part in targets.split(','):
        part = part.strip()
        if '-' in part and '.' in part:
            # 192.168.1.1-192.168.1.254
            start, end = part.split('-', 1)
            start_parts = start.strip().split('.')
            end_parts = end.strip().split('.')
            for i in range(int(start_parts[3]), int(end_parts[3]) + 1):
                ips.append(f'{start_parts[0]}.{start_parts[1]}.{start_parts[2]}.{i}')
        elif '/' in part:
            # CIDR: 192.168.1.0/24
            import ipaddress
            for ip in ipaddress.ip_network(part, strict=False):
                ips.append(str(ip))
        else:
            ips.append(part)
    return ips
