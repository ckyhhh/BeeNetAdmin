"""设备管理视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Device, DeviceGroup, Credential, DeviceInfo, ConfigBackup
from .serializers import (
    DeviceListSerializer, DeviceDetailSerializer, DeviceGroupSerializer,
    CredentialSerializer, DeviceInfoSerializer, ConfigBackupSerializer,
)


class DeviceViewSet(viewsets.ModelViewSet):
    """设备 CRUD"""
    queryset = Device.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return DeviceListSerializer
        return DeviceDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        group = self.request.query_params.get('group')
        dev_status = self.request.query_params.get('status')
        vendor = self.request.query_params.get('vendor')

        if keyword:
            qs = qs.filter(Q(name__icontains=keyword) | Q(ip__icontains=keyword) | Q(hostname__icontains=keyword))
        if group:
            qs = qs.filter(group_id=group)
        if dev_status:
            qs = qs.filter(status=dev_status)
        if vendor:
            qs = qs.filter(vendor__icontains=vendor)
        return qs

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """测试设备连接"""
        device = self.get_object()
        # TODO: 实际测试 SSH/Telnet 连接
        return Response({'message': '连接测试功能待实现'})

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        """采集设备信息"""
        device = self.get_object()
        from .tasks import collect_device_info
        collect_device_info.delay(device.id)
        return Response({'message': '采集任务已提交'})

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """获取设备采集信息"""
        device = self.get_object()
        infos = DeviceInfo.objects.filter(device=device)
        return Response(DeviceInfoSerializer(infos, many=True).data)

    @action(detail=True, methods=['get'], url_path='config/running')
    def running_config(self, request, pk=None):
        """获取运行配置"""
        device = self.get_object()
        backup = ConfigBackup.objects.filter(device=device, config_type='running').first()
        if backup:
            return Response(ConfigBackupSerializer(backup).data)
        return Response({'content': ''})

    @action(detail=True, methods=['get'], url_path='config/startup')
    def startup_config(self, request, pk=None):
        """获取启动配置"""
        device = self.get_object()
        backup = ConfigBackup.objects.filter(device=device, config_type='startup').first()
        if backup:
            return Response(ConfigBackupSerializer(backup).data)
        return Response({'content': ''})

    @action(detail=True, methods=['post'], url_path='config/backup')
    def backup_config(self, request, pk=None):
        """备份配置"""
        device = self.get_object()
        from .tasks import backup_device_config
        backup_device_config.delay(device.id)
        return Response({'message': '备份任务已提交'})

    @action(detail=True, methods=['get'], url_path='config/diff')
    def config_diff(self, request, pk=None):
        """配置对比"""
        device = self.get_object()
        running = ConfigBackup.objects.filter(device=device, config_type='running').first()
        startup = ConfigBackup.objects.filter(device=device, config_type='startup').first()
        return Response({
            'running': running.content if running else '',
            'startup': startup.content if startup else '',
        })

    @action(detail=False, methods=['post'])
    def export(self, request):
        """导出设备信息"""
        # TODO: 可选字段导出
        return Response({'message': '导出功能待实现'})

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """批量删除"""
        ids = request.data.get('ids', [])
        Device.objects.filter(id__in=ids).delete()
        return Response({'message': f'已删除 {len(ids)} 台设备'})


class DeviceGroupViewSet(viewsets.ModelViewSet):
    """设备组 CRUD"""
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer

    @action(detail=True, methods=['post'], url_path='members')
    def add_member(self, request, pk=None):
        """添加设备到组"""
        group = self.get_object()
        device_id = request.data.get('device_id')
        Device.objects.filter(id=device_id).update(group=group)
        return Response({'message': '已添加'})

    @action(detail=True, methods=['delete'], url_path='members/(?P<device_id>[^/.]+)')
    def remove_member(self, request, pk=None, device_id=None):
        """从组中移除设备"""
        Device.objects.filter(id=device_id, group_id=pk).update(group=None)
        return Response({'message': '已移除'})


class CredentialViewSet(viewsets.ModelViewSet):
    """凭据 CRUD"""
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
