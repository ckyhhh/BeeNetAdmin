"""存活检测视图"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AliveTask, AliveResult
from .serializers import AliveTaskSerializer, AliveResultSerializer


class AliveTaskViewSet(viewsets.ModelViewSet):
    queryset = AliveTask.objects.all().order_by('-created_at')
    serializer_class = AliveTaskSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """执行检测"""
        task = self.get_object()
        from .tasks import start_alive_check
        start_alive_check.delay(task.id)
        return Response({'message': '检测任务已提交'})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.enabled = not task.enabled
        task.save(update_fields=['enabled'])
        return Response({'enabled': task.enabled})

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        results = AliveResult.objects.filter(task_id=pk)[:100]
        return Response(AliveResultSerializer(results, many=True).data)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """当前状态概览"""
        task = self.get_object()
        latest = {}
        for did in task.device_ids:
            r = AliveResult.objects.filter(task_id=pk, device_id=did).order_by('-checked_at').first()
            if r:
                latest[did] = AliveResultSerializer(r).data
        return Response(latest)
