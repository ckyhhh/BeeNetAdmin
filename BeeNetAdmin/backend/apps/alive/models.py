"""存活检测模型"""
from django.db import models


class AliveTask(models.Model):
    """存活检测任务"""
    CHECK_TYPE_CHOICES = [
        ('ping', 'Ping'),
        ('tcp', 'TCP'),
        ('both', 'Ping + TCP'),
    ]
    name = models.CharField('任务名称', max_length=128)
    device_ids = models.JSONField('设备ID列表')
    check_type = models.CharField('检测类型', max_length=16, choices=CHECK_TYPE_CHOICES, default='both')
    interval_seconds = models.IntegerField('检测间隔(秒)', default=60)
    timeout_seconds = models.IntegerField('超时(秒)', default=5)
    bandwidth_limit_mbps = models.DecimalField('带宽限制(Mbps)', max_digits=10, decimal_places=2, default=10)
    connection_limit = models.IntegerField('连接数限制', default=10)
    notify_email = models.BooleanField('邮件通知', default=False)
    enabled = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'alive_task'
        verbose_name = '存活检测任务'

    def __str__(self):
        return self.name


class AliveResult(models.Model):
    """存活检测结果"""
    task = models.ForeignKey(AliveTask, on_delete=models.CASCADE, verbose_name='任务')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, verbose_name='设备')
    is_alive = models.BooleanField('是否存活')
    latency_ms = models.DecimalField('延迟(ms)', max_digits=10, decimal_places=2, null=True)
    packet_loss_percent = models.DecimalField('丢包率(%)', max_digits=5, decimal_places=2, null=True)
    bandwidth_usage_mbps = models.DecimalField('带宽使用(Mbps)', max_digits=10, decimal_places=2, null=True)
    connection_count = models.IntegerField('连接数', null=True)
    checked_at = models.DateTimeField('检测时间')

    class Meta:
        db_table = 'alive_result'
        verbose_name = '存活检测结果'
        ordering = ['-checked_at']
