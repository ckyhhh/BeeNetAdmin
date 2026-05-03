"""巡检异步任务 - 三段管道"""
import os
import time
from celery import shared_task
from django.utils import timezone
from django.conf import settings


# ===== 管道入口 =====

@shared_task
def start_inspection(task_id):
    """巡检入口：创建 Result 记录，分发采集任务"""
    from .models import InspectionTask, InspectionResult
    from apps.devices.models import Device

    task = InspectionTask.objects.get(id=task_id)
    template = task.template

    for device_id in task.device_ids:
        device = Device.objects.get(id=device_id)
        commands = _adapt_commands(template, device)

        result = InspectionResult.objects.create(
            task=task, device=device, template=template,
            status='collecting', started_at=timezone.now()
        )
        collect_device_data.delay(result.id, device_id, commands)

    task.status = 'running'
    task.last_run_at = timezone.now()
    task.save(update_fields=['status', 'last_run_at'])


def _adapt_commands(template, device):
    """根据设备厂商适配命令"""
    vendor = (device.vendor or 'default').lower()
    adapted = []
    for cmd_def in template.commands:
        actual = cmd_def.get('commands', {}).get(vendor, cmd_def.get('commands', {}).get('default', ''))
        adapted.append({'cmd': actual, 'alias': cmd_def.get('alias', '')})
    return adapted


# ===== 第一段：采集 =====

@shared_task(bind=True, max_retries=1, default_retry_delay=5,
             queue='collect', rate_limit='60/m')
def collect_device_data(self, result_id, device_id, commands):
    """采集队列：连接 → 执行命令 → 存缓存 → 断开"""
    from .models import InspectionResult
    from apps.devices.models import Device
    from engine.cache import DeviceDataCache
    from engine.ssh import SSHClient
    from engine.telnet import TelnetClient

    cache = DeviceDataCache()
    device = Device.objects.get(id=device_id)

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
                for cmd_info in commands:
                    try:
                        output = client.execute(cmd_info['cmd'], timeout=30)
                        cache.store_raw_output(result_id, device_id, cmd_info['alias'], output or '')
                    except Exception as e:
                        cache.store_raw_output(result_id, device_id, cmd_info['alias'], f'ERROR: {e}')
            finally:
                client.close()

        _update_result_status(result_id, 'collected')
        parse_device_data.delay(result_id, device_id)

    except Exception as e:
        _update_result_status(result_id, 'collect_failed', str(e))
    finally:
        cache.release_device_lock(device_id)


# ===== 第二段：解析 =====

@shared_task(queue='parse')
def parse_device_data(result_id, device_id):
    """解析队列：从 Redis 读取原始输出 → TextFSM 解析 → 存入 DB"""
    from .models import InspectionResult
    from engine.cache import DeviceDataCache
    from engine.textfsm_parser import TextFSMParser

    cache = DeviceDataCache()
    textfsm = TextFSMParser()
    result = InspectionResult.objects.get(id=result_id)
    template = result.template

    raw_outputs = cache.get_raw_outputs(result_id, device_id)
    if not raw_outputs:
        _update_result_status(result_id, 'parse_failed', '缓存已过期')
        return

    parsed_data = {}
    for cmd_def in template.commands:
        alias = cmd_def.get('alias', '')
        fsm = cmd_def.get('fsm')
        raw = raw_outputs.get(alias, b'').decode('utf-8', errors='replace') if isinstance(raw_outputs.get(alias), bytes) else str(raw_outputs.get(alias, ''))

        if raw.startswith('ERROR:'):
            parsed_data[alias] = {'error': raw}
            continue

        if fsm:
            try:
                parsed_data[alias] = textfsm.parse(template.vendor or 'generic', fsm, raw)
            except Exception as e:
                parsed_data[alias] = {'error': str(e)}
        else:
            parsed_data[alias] = {'raw': raw}

    from apps.devices.models import Device
    device = Device.objects.get(id=device_id)
    parsed_data['_device'] = {
        'name': device.name, 'ip': device.ip,
        'vendor': device.vendor, 'model': device.model,
        'hostname': device.hostname, 'os_version': device.os_version,
    }
    parsed_data['_meta'] = {
        'result_id': result_id, 'device_id': device_id,
        'generated_at': timezone.now().isoformat(),
    }

    cache.store_parsed_data(result_id, device_id, parsed_data)
    result.parsed_data = parsed_data
    result.status = 'parsed'
    result.save(update_fields=['parsed_data', 'status'])
    cache.delete_raw_outputs(result_id, device_id)

    render_inspection.delay(result_id, device_id)


# ===== 第三段：渲染 =====

@shared_task(queue='render')
def render_inspection(result_id, device_id):
    """渲染队列：从 Redis 读取解析数据 → Jinja2 渲染 → 生成报告"""
    from .models import InspectionResult, InspectionTask
    from engine.cache import DeviceDataCache
    from engine.jinja2_renderer import Jinja2Renderer

    cache = DeviceDataCache()
    jinja2 = Jinja2Renderer()
    result = InspectionResult.objects.get(id=result_id)

    parsed_data = cache.get_parsed_data(result_id, device_id) or result.parsed_data
    if not parsed_data:
        _update_result_status(result_id, 'render_failed', '解析数据不存在')
        return

    tpl_name = result.template.jinja2_template_name or 'inspection_basic.txt.j2'
    try:
        report = jinja2.render(tpl_name, parsed_data)
    except Exception as e:
        _update_result_status(result_id, 'render_failed', str(e))
        return

    report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(report_dir, exist_ok=True)
    filename = f'inspection_{result_id}_{device_id}_{int(time.time())}.txt'
    path = os.path.join(report_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)

    result.report_content = report
    result.report_file_path = path
    result.status = 'success'
    result.finished_at = timezone.now()
    result.save()
    cache.delete_parsed_data(result_id, device_id)

    _check_task_completion(result.task_id)


def _check_task_completion(task_id):
    """检查任务是否全部完成"""
    from .models import InspectionResult, InspectionTask
    from apps.notification.tasks import send_notification

    total = InspectionResult.objects.filter(task_id=task_id).count()
    done = InspectionResult.objects.filter(
        task_id=task_id,
        status__in=['success', 'collect_failed', 'parse_failed', 'render_failed']
    ).count()

    if done >= total:
        task = InspectionTask.objects.get(id=task_id)
        task.status = 'completed'
        task.save(update_fields=['status'])
        ok = InspectionResult.objects.filter(task_id=task_id, status='success').count()
        send_notification.delay(
            ntype='inspection_complete',
            title=f'巡检完成: {task.name}',
            message=f'共 {total} 台，成功 {ok} 台，失败 {total - ok} 台'
        )


def _update_result_status(result_id, status, error=''):
    from .models import InspectionResult
    InspectionResult.objects.filter(id=result_id).update(
        status=status, error_message=error
    )
