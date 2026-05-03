"""终端连接模型"""
from django.db import models


class InstantLoginRecord(models.Model):
    """即时登录记录"""
    host = models.CharField('主机', max_length=256)
    port = models.IntegerField('端口')
    login_method = models.CharField('登录方式', max_length=16)
    username = models.CharField('用户名', max_length=128)
    recorded = models.BooleanField('已录制', default=True)
    log_path = models.CharField('日志路径', max_length=512, blank=True)
    duration_seconds = models.IntegerField('时长(秒)', null=True)
    connected_at = models.DateTimeField('连接时间', null=True)
    disconnected_at = models.DateTimeField('断开时间', null=True)

    class Meta:
        db_table = 'instant_login_record'
        verbose_name = '登录记录'
        ordering = ['-connected_at']
