"""通知视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification, EmailConfig
from .serializers import NotificationSerializer, EmailConfigSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        is_read = self.request.query_params.get('is_read')
        ntype = self.request.query_params.get('type')
        if is_read is not None:
            qs = qs.filter(is_read=is_read == 'true')
        if ntype:
            qs = qs.filter(type=ntype)
        return qs

    @action(detail=True, methods=['put'], url_path='read')
    def mark_read(self, request, pk=None):
        """标记已读"""
        self.get_object()
        Notification.objects.filter(id=pk).update(is_read=True)
        return Response({'message': '已标记'})

    @action(detail=False, methods=['post'], url_path='read-all')
    def mark_all_read(self, request):
        """全部已读"""
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({'message': '全部已标记'})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def email_config(request):
    """邮件配置"""
    config = EmailConfig.objects.first()
    if request.method == 'GET':
        if config:
            return Response(EmailConfigSerializer(config).data)
        return Response({})

    serializer = EmailConfigSerializer(config, data=request.data, partial=True) if config else EmailConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def email_test(request):
    """测试邮件"""
    # TODO: 发送测试邮件
    return Response({'message': '测试邮件已发送'})
