"""设备扫描模型"""
from django.db import models


class ScanTask(models.Model):
    """扫描任务"""
    SCAN_TYPE_CHOICES = [
        ('periodic', '周期执行'),
        ('interval', '间隔执行'),
        ('manual', '手动执行'),
    ]
    name = models.CharField('任务名称', max_length=128)
    targets = models.TextField('目标地址')
    scan_type = models.CharField('扫描类型', max_length=16, choices=SCAN_TYPE_CHOICES, default='manual')
    cron_expr = models.CharField('Cron表达式', max_length=128, blank=True)
    interval_seconds = models.IntegerField('间隔秒数', null=True)
    credential = models.ForeignKey('devices.Credential', on_delete=models.SET_NULL, null=True, verbose_name='凭据')
    port = models.IntegerField('端口', default=22)
    auto_add = models.BooleanField('自动入库', default=True)
    auto_verify = models.BooleanField('自动验证', default=True)
    enabled = models.BooleanField('启用', default=True)
    last_run_at = models.DateTimeField('上次执行', null=True)
    next_run_at = models.DateTimeField('下次执行', null=True)
    status = models.CharField('状态', max_length=16, default='idle')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'scan_task'
        verbose_name = '扫描任务'

    def __str__(self):
        return self.name


class ScanResult(models.Model):
    """扫描结果"""
    STATUS_CHOICES = [
        ('found', '已发现'),
        ('not_found', '未发现'),
        ('error', '错误'),
    ]
    task = models.ForeignKey(ScanTask, on_delete=models.CASCADE, verbose_name='任务')
    ip = models.GenericIPAddressField('IP地址')
    port = models.IntegerField('端口')
    status = models.CharField('状态', max_length=16, choices=STATUS_CHOICES)
    vendor = models.CharField('厂商', max_length=64, blank=True)
    model = models.CharField('型号', max_length=128, blank=True)
    os_version = models.CharField('OS版本', max_length=256, blank=True)
    hostname = models.CharField('主机名', max_length=256, blank=True)
    device = models.ForeignKey('devices.Device', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联设备')
    raw_output = models.TextField('原始输出', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'scan_result'
        verbose_name = '扫描结果'
