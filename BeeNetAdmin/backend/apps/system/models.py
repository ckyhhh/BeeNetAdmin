"""系统设置模型"""
from django.db import models


class SystemSetting(models.Model):
    """系统设置"""
    key = models.CharField('键', max_length=128, primary_key=True)
    value = models.TextField('值')
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'system_setting'
        verbose_name = '系统设置'


class AutoBackupConfig(models.Model):
    """自动备份配置"""
    backup_running_config = models.BooleanField('备份运行配置', default=True)
    backup_startup_config = models.BooleanField('备份启动配置', default=True)
    schedule_type = models.CharField('调度类型', max_length=16, default='daily')
    cron_expr = models.CharField('Cron表达式', max_length=128, default='0 2 * * *')
    enabled = models.BooleanField('启用', default=True)
    last_run_at = models.DateTimeField('上次执行', null=True)
    next_run_at = models.DateTimeField('下次执行', null=True)

    class Meta:
        db_table = 'auto_backup_config'
        verbose_name = '自动备份配置'
