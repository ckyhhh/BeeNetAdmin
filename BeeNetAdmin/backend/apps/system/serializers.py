"""系统设置序列化器"""
from rest_framework import serializers
from .models import SystemSetting, AutoBackupConfig


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'


class AutoBackupConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoBackupConfig
        fields = '__all__'
