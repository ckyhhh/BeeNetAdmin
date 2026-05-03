"""设备管理 Admin"""
from django.contrib import admin
from .models import Device, DeviceGroup, Credential, DeviceInfo, ConfigBackup

admin.site.register(Device)
admin.site.register(DeviceGroup)
admin.site.register(Credential)
admin.site.register(DeviceInfo)
admin.site.register(ConfigBackup)
