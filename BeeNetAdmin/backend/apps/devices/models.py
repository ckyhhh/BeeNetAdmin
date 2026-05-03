"""设备管理模型"""
from django.db import models


class DeviceGroup(models.Model):
    """设备组"""
    name = models.CharField('组名', max_length=128)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'device_group'
        verbose_name = '设备组'

    def __str__(self):
        return self.name


class Credential(models.Model):
    """登录凭据"""
    LOGIN_METHOD_CHOICES = [
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
    ]
    name = models.CharField('凭据名称', max_length=128)
    login_method = models.CharField('登录方式', max_length=16, choices=LOGIN_METHOD_CHOICES)
    username = models.CharField('用户名', max_length=128)
    password = models.TextField('密码（加密）')
    enable_password = models.TextField('Enable密码（加密）', blank=True)
    ssh_key = models.TextField('SSH密钥（加密）', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'credential'
        verbose_name = '登录凭据'

    def __str__(self):
        return f'{self.name} ({self.login_method})'


class Device(models.Model):
    """网络设备"""
    DEVICE_TYPE_CHOICES = [
        ('router', '路由器'),
        ('switch', '交换机'),
        ('firewall', '防火墙'),
        ('other', '其他'),
    ]
    STATUS_CHOICES = [
        ('online', '在线'),
        ('offline', '离线'),
        ('unknown', '未知'),
    ]
    name = models.CharField('设备名称', max_length=128, unique=True)
    ip = models.GenericIPAddressField('IP地址')
    port = models.IntegerField('端口', default=22)
    device_type = models.CharField('设备类型', max_length=32, choices=DEVICE_TYPE_CHOICES, default='switch')
    vendor = models.CharField('厂商', max_length=64, blank=True)
    model = models.CharField('型号', max_length=128, blank=True)
    os_version = models.CharField('OS版本', max_length=256, blank=True)
    serial_number = models.CharField('序列号', max_length=128, blank=True)
    hostname = models.CharField('主机名', max_length=256, blank=True)
    login_method = models.CharField('登录方式', max_length=16, default='ssh')
    credential = models.ForeignKey(Credential, on_delete=models.SET_NULL, null=True, verbose_name='凭据')
    group = models.ForeignKey(DeviceGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='设备组')
    status = models.CharField('状态', max_length=16, choices=STATUS_CHOICES, default='unknown')
    uptime = models.CharField('运行时间', max_length=256, blank=True)
    cpu_usage = models.DecimalField('CPU使用率', max_digits=5, decimal_places=2, null=True)
    memory_usage = models.DecimalField('内存使用率', max_digits=5, decimal_places=2, null=True)
    interface_count = models.IntegerField('接口数', null=True)
    bandwidth_mbps = models.DecimalField('带宽(Mbps)', max_digits=10, decimal_places=2, null=True)
    last_seen_at = models.DateTimeField('最后在线', null=True)
    last_inspection_at = models.DateTimeField('最后巡检', null=True)
    last_backup_at = models.DateTimeField('最后备份', null=True)
    notes = models.TextField('备注', blank=True)
    tags = models.CharField('标签', max_length=512, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'device'
        verbose_name = '设备'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.ip})'


class DeviceInfo(models.Model):
    """设备采集信息"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='设备')
    info_type = models.CharField('信息类型', max_length=64)
    data = models.JSONField('数据')
    collected_at = models.DateTimeField('采集时间')

    class Meta:
        db_table = 'device_info'
        verbose_name = '设备信息'


class ConfigBackup(models.Model):
    """配置备份"""
    CONFIG_TYPE_CHOICES = [
        ('running', '运行配置'),
        ('startup', '启动配置'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='设备')
    config_type = models.CharField('配置类型', max_length=16, choices=CONFIG_TYPE_CHOICES)
    content = models.TextField('配置内容')
    version = models.IntegerField('版本号')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'config_backup'
        verbose_name = '配置备份'
        ordering = ['-version']
