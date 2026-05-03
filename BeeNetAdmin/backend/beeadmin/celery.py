"""
Celery 应用配置
"""
import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beeadmin.settings.dev')

app = Celery('beeadmin')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 队列定义
app.conf.task_queues = (
    Queue('collect',  Exchange('collect'),  routing_key='collect'),
    Queue('parse',    Exchange('parse'),    routing_key='parse'),
    Queue('render',   Exchange('render'),   routing_key='render'),
    Queue('alive',    Exchange('alive'),    routing_key='alive'),
    Queue('scan',     Exchange('scan'),     routing_key='scan'),
    Queue('notify',   Exchange('notify'),   routing_key='notify'),
    Queue('default',  Exchange('default'),  routing_key='default'),
)

# 路由规则
app.conf.task_routes = {
    'apps.inspection.tasks.collect_device_data':    {'queue': 'collect'},
    'apps.inspection.tasks.parse_device_data':      {'queue': 'parse'},
    'apps.inspection.tasks.render_inspection':      {'queue': 'render'},
    'apps.alive.tasks.*':                           {'queue': 'alive'},
    'apps.scanning.tasks.*':                        {'queue': 'scan'},
    'apps.notification.tasks.*':                    {'queue': 'notify'},
    'apps.devices.tasks.collect_device_info':       {'queue': 'collect'},
    'apps.devices.tasks.backup_device_config':      {'queue': 'collect'},
    'apps.system.tasks.*':                          {'queue': 'default'},
}

app.autodiscover_tasks()
