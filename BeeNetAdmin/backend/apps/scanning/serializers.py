"""扫描序列化器"""
from rest_framework import serializers
from .models import ScanTask, ScanResult


class ScanTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanTask
        fields = '__all__'


class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = '__all__'
