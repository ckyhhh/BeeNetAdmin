"""巡检 URL"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('inspection/templates', views.InspectionTemplateViewSet, basename='inspection-template')
router.register('inspection/tasks', views.InspectionTaskViewSet, basename='inspection-task')
router.register('inspection/results', views.InspectionResultViewSet, basename='inspection-result')

urlpatterns = [
    path('', include(router.urls)),
]
