"""系统设置视图"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import SystemSetting, AutoBackupConfig
from .serializers import SystemSettingSerializer, AutoBackupConfigSerializer


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def system_settings(request):
    """系统设置"""
    if request.method == 'GET':
        settings = SystemSetting.objects.all()
        return Response(SystemSettingSerializer(settings, many=True).data)
    # PUT: 批量更新
    for key, value in request.data.items():
        SystemSetting.objects.update_or_create(key=key, defaults={'value': value})
    return Response({'message': '设置已更新'})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def auto_backup(request):
    """自动备份配置"""
    config = AutoBackupConfig.objects.first()
    if request.method == 'GET':
        if config:
            return Response(AutoBackupConfigSerializer(config).data)
        return Response({})
    serializer = AutoBackupConfigSerializer(config, data=request.data, partial=True) if config else AutoBackupConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check(request):
    """健康检查"""
    from django.db import connections
    from django.core.cache import cache

    result = {'status': 'ok', 'services': {}}

    # MySQL
    try:
        connections['default'].cursor()
        result['services']['mysql'] = 'ok'
    except Exception:
        result['services']['mysql'] = 'error'
        result['status'] = 'degraded'

    # Redis
    try:
        cache.set('health_check', 'ok', 10)
        result['services']['redis'] = 'ok'
    except Exception:
        result['services']['redis'] = 'error'
        result['status'] = 'degraded'

    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def backup_now(request):
    """立即备份"""
    from apps.devices.models import Device
    from apps.devices.tasks import backup_device_config
    devices = Device.objects.all()
    for device in devices:
        backup_device_config.delay(device.id)
    return Response({'message': f'已提交 {devices.count()} 台设备的备份任务'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def textfsm_templates(request):
    """获取 TextFSM 模板列表"""
    import os
    from django.conf import settings
    template_dir = os.path.join(settings.BASE_DIR.parent, 'templates', 'textfsm')
    templates = []
    if os.path.exists(template_dir):
        for vendor in os.listdir(template_dir):
            vendor_dir = os.path.join(template_dir, vendor)
            if os.path.isdir(vendor_dir):
                for f in os.listdir(vendor_dir):
                    if f.endswith('.textfsm'):
                        templates.append({'vendor': vendor, 'name': f, 'path': f'{vendor}/{f}'})
    return Response(templates)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def jinja2_templates(request):
    """获取 Jinja2 模板列表"""
    import os
    from django.conf import settings
    template_dir = os.path.join(settings.BASE_DIR.parent, 'templates', 'jinja2')
    templates = []
    if os.path.exists(template_dir):
        for f in os.listdir(template_dir):
            if f.endswith('.j2'):
                templates.append({'name': f, 'path': f})
    return Response(templates)
