"""巡检管理模型"""
from django.db import models


class InspectionTemplate(models.Model):
    """巡检模板"""
    name = models.CharField('模板名称', max_length=128)
    description = models.TextField('描述', blank=True)
    vendor = models.CharField('厂商', max_length=64, blank=True)
    commands = models.JSONField('命令列表')
    textfsm_mapping = models.JSONField('TextFSM映射', default=dict)
    jinja2_template_name = models.CharField('Jinja2模板', max_length=256, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'inspection_template'
        verbose_name = '巡检模板'

    def __str__(self):
        return self.name


class InspectionTask(models.Model):
    """巡检任务"""
    SCHEDULE_TYPE_CHOICES = [
        ('periodic', '周期执行'),
        ('manual', '手动执行'),
    ]
    name = models.CharField('任务名称', max_length=128)
    device_ids = models.JSONField('设备ID列表')
    template = models.ForeignKey(InspectionTemplate, on_delete=models.CASCADE, verbose_name='模板')
    schedule_type = models.CharField('调度类型', max_length=16, choices=SCHEDULE_TYPE_CHOICES, default='manual')
    cron_expr = models.CharField('Cron表达式', max_length=128, blank=True)
    enabled = models.BooleanField('启用', default=True)
    status = models.CharField('状态', max_length=16, default='idle')
    last_run_at = models.DateTimeField('上次执行', null=True)
    next_run_at = models.DateTimeField('下次执行', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'inspection_task'
        verbose_name = '巡检任务'

    def __str__(self):
        return self.name


class InspectionResult(models.Model):
    """巡检结果"""
    STATUS_CHOICES = [
        ('collecting', '采集中'),
        ('collected', '采集完成'),
        ('parsing', '解析中'),
        ('parsed', '解析完成'),
        ('rendering', '渲染中'),
        ('success', '成功'),
        ('collect_failed', '采集失败'),
        ('parse_failed', '解析失败'),
        ('render_failed', '渲染失败'),
    ]
    task = models.ForeignKey(InspectionTask, on_delete=models.CASCADE, verbose_name='任务')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, verbose_name='设备')
    template = models.ForeignKey(InspectionTemplate, on_delete=models.CASCADE, verbose_name='模板')
    parsed_data = models.JSONField('解析数据', null=True)
    report_content = models.TextField('报告内容', blank=True)
    report_file_path = models.CharField('报告路径', max_length=512, blank=True)
    status = models.CharField('状态', max_length=16, choices=STATUS_CHOICES, default='collecting')
    error_message = models.TextField('错误信息', blank=True)
    started_at = models.DateTimeField('开始时间', null=True)
    finished_at = models.DateTimeField('完成时间', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'inspection_result'
        verbose_name = '巡检结果'
