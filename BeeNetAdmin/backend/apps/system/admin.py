"""系统 Admin"""
from django.contrib import admin
from .models import SystemSetting, AutoBackupConfig

admin.site.register(SystemSetting)
admin.site.register(AutoBackupConfig)
