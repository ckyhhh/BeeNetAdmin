"""巡检视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InspectionTemplate, InspectionTask, InspectionResult
from .serializers import InspectionTemplateSerializer, InspectionTaskSerializer, InspectionResultSerializer


class InspectionTemplateViewSet(viewsets.ModelViewSet):
    queryset = InspectionTemplate.objects.all().order_by('-created_at')
    serializer_class = InspectionTemplateSerializer

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """克隆模板"""
        template = self.get_object()
        template.pk = None
        template.name = f'{template.name} (副本)'
        template.save()
        return Response(InspectionTemplateSerializer(template).data)


class InspectionTaskViewSet(viewsets.ModelViewSet):
    queryset = InspectionTask.objects.all().order_by('-created_at')
    serializer_class = InspectionTaskSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """执行巡检"""
        task = self.get_object()
        from .tasks import start_inspection
        start_inspection.delay(task.id)
        return Response({'message': '巡检任务已提交'})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """启用/禁用"""
        task = self.get_object()
        task.enabled = not task.enabled
        task.save(update_fields=['enabled'])
        return Response({'enabled': task.enabled})

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """获取巡检结果"""
        results = InspectionResult.objects.filter(task_id=pk)
        return Response(InspectionResultSerializer(results, many=True).data)


class InspectionResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InspectionResult.objects.all().order_by('-created_at')
    serializer_class = InspectionResultSerializer

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """获取报告"""
        result = self.get_object()
        return Response({'content': result.report_content})

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """导出报告"""
        result = self.get_object()
        # TODO: 生成文件下载
        return Response({'content': result.report_content})
