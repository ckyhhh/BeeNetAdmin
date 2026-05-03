"""用户认证视图"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录"""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def setup_view(request):
    """首次初始化：创建管理员"""
    if User.objects.filter(is_superuser=True).exists():
        return Response({'error': '管理员已存在'}, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username', 'admin')
    password = request.data.get('password')
    if not password or len(password) < 8:
        return Response({'error': '密码至少8位'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_superuser(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def setup_status(request):
    """检查是否已初始化"""
    return Response({'initialized': User.objects.filter(is_superuser=True).exists()})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """当前用户信息"""
    return Response(UserSerializer(request.user).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not request.user.check_password(serializer.validated_data['old_password']):
        return Response({'error': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()
    return Response({'message': '密码修改成功'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_view(request):
    """解锁主密码"""
    master_password = request.data.get('master_password')
    if not master_password:
        return Response({'error': '请输入主密码'}, status=status.HTTP_400_BAD_REQUEST)
    # TODO: 验证主密码哈希
    return Response({'message': '解锁成功'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lock_view(request):
    """锁定"""
    # TODO: 清除 Redis 中的主密码缓存
    return Response({'message': '已锁定'})
