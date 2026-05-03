"""存活检测序列化器"""
from rest_framework import serializers
from .models import AliveTask, AliveResult


class AliveTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliveTask
        fields = '__all__'


class AliveResultSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_ip = serializers.CharField(source='device.ip', read_only=True)

    class Meta:
        model = AliveResult
        fields = '__all__'
