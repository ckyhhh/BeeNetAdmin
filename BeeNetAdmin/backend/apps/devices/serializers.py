"""设备管理序列化器"""
from rest_framework import serializers
from .models import Device, DeviceGroup, Credential, DeviceInfo, ConfigBackup


class DeviceGroupSerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField()

    class Meta:
        model = DeviceGroup
        fields = '__all__'

    def get_device_count(self, obj):
        return Device.objects.filter(group=obj).count()


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'enable_password': {'write_only': True}, 'ssh_key': {'write_only': True}}


class DeviceListSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, default='')
    credential_name = serializers.CharField(source='credential.name', read_only=True, default='')

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'ip', 'port', 'device_type', 'vendor', 'model',
            'os_version', 'hostname', 'status', 'login_method', 'group',
            'group_name', 'credential', 'credential_name', 'cpu_usage',
            'memory_usage', 'last_seen_at', 'last_inspection_at', 'last_backup_at',
            'tags', 'created_at', 'updated_at',
        ]


class DeviceDetailSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, default='')

    class Meta:
        model = Device
        fields = '__all__'


class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = '__all__'


class ConfigBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigBackup
        fields = '__all__'
