"""存活检测异步任务"""
from celery import shared_task
from django.utils import timezone


@shared_task
def start_alive_check(task_id):
    """存活检测入口"""
    from .models import AliveTask, AliveResult
    from apps.devices.models import Device

    task = AliveTask.objects.get(id=task_id)
    last = {}
    for did in task.device_ids:
        r = AliveResult.objects.filter(task_id=task_id, device_id=did).order_by('-checked_at').first()
        if r:
            last[did] = r.is_alive

    for did in task.device_ids:
        device = Device.objects.get(id=did)
        alive_check_device.delay(
            task_id=task_id, device_id=did, device_ip=device.ip,
            check_type=task.check_type, timeout=task.timeout_seconds,
            last_alive=last.get(did), notify_email=task.notify_email,
            connection_limit=task.connection_limit,
        )


@shared_task(queue='alive', rate_limit='30/m', soft_time_limit=30, time_limit=35)
def alive_check_device(task_id, device_id, device_ip, check_type,
                       timeout, last_alive, notify_email, connection_limit):
    """单设备存活检测"""
    from .models import AliveResult
    from apps.devices.models import Device
    from apps.notification.tasks import send_notification
    from engine.cache import DeviceDataCache
    from engine.ping import PingChecker
    from engine.tcp_check import TCPChecker

    cache = DeviceDataCache()
    current = cache.incr_alive_connections()
    if current > connection_limit:
        cache.decr_alive_connections()
        return

    try:
        is_alive = False
        latency = None
        loss = None

        if check_type in ('ping', 'both'):
            r = PingChecker().ping(device_ip, count=3, timeout=timeout)
            if r['success']:
                is_alive = True
                latency = r['latency_ms']
                loss = r['packet_loss']

        if check_type in ('tcp', 'both'):
            r = TCPChecker().check(device_ip, port=22, timeout=timeout)
            if r['is_alive']:
                is_alive = True
                if latency is None:
                    latency = r['latency_ms']

        AliveResult.objects.create(
            task_id=task_id, device_id=device_id,
            is_alive=is_alive, latency_ms=latency,
            packet_loss_percent=loss, checked_at=timezone.now()
        )

        if last_alive is not None:
            device = Device.objects.get(id=device_id)
            if last_alive and not is_alive:
                device.status = 'offline'
                device.save(update_fields=['status'])
                send_notification.delay(
                    ntype='device_offline',
                    title=f'设备离线: {device.name}',
                    message=f'{device.name} ({device.ip}) 已离线',
                )
            elif not last_alive and is_alive:
                device.status = 'online'
                device.last_seen_at = timezone.now()
                device.save(update_fields=['status', 'last_seen_at'])
                send_notification.delay(
                    ntype='device_online',
                    title=f'设备上线: {device.name}',
                    message=f'{device.name} ({device.ip}) 已恢复在线',
                )
    finally:
        cache.decr_alive_connections()
