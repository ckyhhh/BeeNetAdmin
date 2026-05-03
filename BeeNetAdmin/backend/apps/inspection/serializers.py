"""巡检序列化器"""
from rest_framework import serializers
from .models import InspectionTemplate, InspectionTask, InspectionResult


class InspectionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionTemplate
        fields = '__all__'


class InspectionTaskSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)

    class Meta:
        model = InspectionTask
        fields = '__all__'


class InspectionResultSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_ip = serializers.CharField(source='device.ip', read_only=True)

    class Meta:
        model = InspectionResult
        fields = '__all__'
