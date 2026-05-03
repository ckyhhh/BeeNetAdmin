"""设备管理 URL"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('devices', views.DeviceViewSet)
router.register('device-groups', views.DeviceGroupViewSet)
router.register('credentials', views.CredentialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
