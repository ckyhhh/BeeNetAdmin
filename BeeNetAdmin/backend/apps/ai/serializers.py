"""AI 序列化器"""
from rest_framework import serializers
from .models import AIConfig


class AIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfig
        fields = '__all__'
        extra_kwargs = {'api_key': {'write_only': True}}
