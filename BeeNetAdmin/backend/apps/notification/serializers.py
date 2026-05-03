"""通知序列化器"""
from rest_framework import serializers
from .models import Notification, EmailConfig


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = '__all__'
        extra_kwargs = {'sender_password': {'write_only': True}}
