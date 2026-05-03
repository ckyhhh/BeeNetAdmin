"""设备管理异步任务"""
from celery import shared_task
from django.utils import timezone


@shared_task(bind=True, max_retries=1, queue='collect')
def collect_device_info(self, device_id):
    """采集设备信息"""
    from .models import Device, DeviceInfo
    from engine.ssh import SSHClient
    from engine.telnet import TelnetClient
    from engine.crypto import CryptoManager
    from engine.device_detector import DeviceDetector

    device = Device.objects.get(id=device_id)
    credential = device.credential
    crypto = CryptoManager()
    # TODO: 获取主密码并解密
    password = credential.password  # 临时

    client = None
    try:
        if device.login_method == 'ssh':
            client = SSHClient()
            client.connect(device.ip, device.port or 22, credential.username, password)
        elif device.login_method == 'telnet':
            client = TelnetClient()
            client.connect(device.ip, device.port or 23, credential.username, password)

        if client:
            # 采集版本信息
            vendor = (device.vendor or '').lower()
            if 'huawei' in vendor:
                raw = client.execute('display version', timeout=15)
            else:
                raw = client.execute('show version', timeout=15)

            if raw:
                detector = DeviceDetector()
                info = detector.parse(raw)
                # 更新设备信息
                for key in ['vendor', 'model', 'os_version', 'hostname', 'serial_number']:
                    if info.get(key):
                        setattr(device, key, info[key])
                device.status = 'online'
                device.last_seen_at = timezone.now()
                device.save()

                DeviceInfo.objects.create(
                    device=device,
                    info_type='version',
                    data=info,
                    collected_at=timezone.now(),
                )
    except Exception as e:
        device.status = 'offline'
        device.save(update_fields=['status'])
        raise
    finally:
        if client:
            client.close()


@shared_task(bind=True, max_retries=1, queue='collect')
def backup_device_config(self, device_id):
    """备份设备配置"""
    from .models import Device, ConfigBackup
    from engine.ssh import SSHClient
    from engine.telnet import TelnetClient
    from engine.config_manager import ConfigManager
    from engine.cache import DeviceDataCache

    device = Device.objects.get(id=device_id)
    cache = DeviceDataCache()

    if not cache.acquire_device_lock(device_id):
        raise self.retry(countdown=5)

    try:
        credential = device.credential
        password = credential.password  # TODO: 解密

        client = None
        if device.login_method == 'ssh':
            client = SSHClient()
            client.connect(device.ip, device.port or 22, credential.username, password)
        elif device.login_method == 'telnet':
            client = TelnetClient()
            client.connect(device.ip, device.port or 23, credential.username, password)

        if client:
            try:
                cm = ConfigManager()
                vendor = device.vendor or 'default'

                running = cm.get_running_config(client, vendor)
                if running:
                    v = ConfigBackup.objects.filter(device_id=device_id, config_type='running').count() + 1
                    ConfigBackup.objects.create(device=device, config_type='running', content=running, version=v)

                startup = cm.get_startup_config(client, vendor)
                if startup:
                    v = ConfigBackup.objects.filter(device_id=device_id, config_type='startup').count() + 1
                    ConfigBackup.objects.create(device=device, config_type='startup', content=startup, version=v)

                device.last_backup_at = timezone.now()
                device.save(update_fields=['last_backup_at'])
            finally:
                client.close()
    finally:
        cache.release_device_lock(device_id)
