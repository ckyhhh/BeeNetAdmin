"""扫描 URL"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('scanning/tasks', views.ScanTaskViewSet, basename='scan-task')
router.register('scanning/results', views.ScanResultViewSet, basename='scan-result')

urlpatterns = [
    path('', include(router.urls)),
]
