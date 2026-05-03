"""扫描视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ScanTask, ScanResult
from .serializers import ScanTaskSerializer, ScanResultSerializer


class ScanTaskViewSet(viewsets.ModelViewSet):
    queryset = ScanTask.objects.all().order_by('-created_at')
    serializer_class = ScanTaskSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """执行扫描"""
        task = self.get_object()
        from .tasks import start_scan
        start_scan.delay(task.id)
        return Response({'message': '扫描任务已提交'})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """启用/禁用"""
        task = self.get_object()
        task.enabled = not task.enabled
        task.save(update_fields=['enabled'])
        return Response({'enabled': task.enabled})

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """获取扫描结果"""
        results = ScanResult.objects.filter(task_id=pk)
        return Response(ScanResultSerializer(results, many=True).data)


class ScanResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScanResult.objects.all().order_by('-created_at')
    serializer_class = ScanResultSerializer
