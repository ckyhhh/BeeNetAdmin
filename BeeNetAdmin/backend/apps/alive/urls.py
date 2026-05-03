"""存活检测 URL"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('alive/tasks', views.AliveTaskViewSet, basename='alive-task')

urlpatterns = [
    path('', include(router.urls)),
]
