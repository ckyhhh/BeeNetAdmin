"""通知管理模型"""
from django.db import models


class Notification(models.Model):
    """通知消息"""
    TYPE_CHOICES = [
        ('device_online', '设备上线'),
        ('device_offline', '设备离线'),
        ('scan_complete', '扫描完成'),
        ('inspection_complete', '巡检完成'),
        ('alive_alert', '存活告警'),
    ]
    type = models.CharField('类型', max_length=32, choices=TYPE_CHOICES)
    title = models.CharField('标题', max_length=256)
    message = models.TextField('内容')
    device = models.ForeignKey('devices.Device', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联设备')
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'notification'
        verbose_name = '通知'
        ordering = ['-created_at']


class EmailConfig(models.Model):
    """邮件配置"""
    smtp_host = models.CharField('SMTP主机', max_length=256)
    smtp_port = models.IntegerField('端口', default=465)
    use_tls = models.BooleanField('使用TLS', default=True)
    sender_email = models.CharField('发件人', max_length=256)
    sender_password = models.TextField('密码（加密）')
    enabled = models.BooleanField('启用', default=False)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'email_config'
        verbose_name = '邮件配置'
