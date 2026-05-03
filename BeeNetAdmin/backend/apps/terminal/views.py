"""终端视图"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InstantLoginRecord


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instant_history(request):
    """即时登录历史"""
    records = InstantLoginRecord.objects.all()[:50]
    data = [{
        'id': r.id, 'host': r.host, 'port': r.port,
        'login_method': r.login_method, 'username': r.username,
        'connected_at': r.connected_at, 'disconnected_at': r.disconnected_at,
        'duration_seconds': r.duration_seconds,
    } for r in records]
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def instant_delete(request, pk):
    """删除登录记录"""
    InstantLoginRecord.objects.filter(id=pk).delete()
    return Response({'message': '已删除'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instant_log(request, pk):
    """获取操作日志"""
    record = InstantLoginRecord.objects.filter(id=pk).first()
    if not record or not record.log_path:
        return Response({'log': ''})
    try:
        with open(record.log_path, 'r', encoding='utf-8') as f:
            return Response({'log': f.read()})
    except FileNotFoundError:
        return Response({'log': ''})
