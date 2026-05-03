"""AI 助手视图"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import AIConfig
from .serializers import AIConfigSerializer


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def ai_config(request):
    """AI 配置"""
    config = AIConfig.objects.first()
    if request.method == 'GET':
        if config:
            return Response(AIConfigSerializer(config).data)
        return Response({})

    serializer = AIConfigSerializer(config, data=request.data, partial=True) if config else AIConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_analyze_terminal(request):
    """分析终端输出"""
    output = request.data.get('output', '')
    if not output:
        return Response({'error': '无输出内容'}, status=status.HTTP_400_BAD_REQUEST)

    config = AIConfig.objects.first()
    if not config:
        return Response({'error': 'AI 未配置'}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: 调用 DeepSeek API 分析
    return Response({'analysis': 'AI 分析功能待实现', 'output': output[:500]})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    """AI 对话"""
    message = request.data.get('message', '')
    if not message:
        return Response({'error': '消息为空'}, status=status.HTTP_400_BAD_REQUEST)

    config = AIConfig.objects.first()
    if not config:
        return Response({'error': 'AI 未配置'}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: 调用 DeepSeek API
    return Response({'reply': f'收到: {message}', 'model': config.model})
