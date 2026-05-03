"""通知 URL"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('notifications/email-config/', views.email_config, name='email-config'),
    path('notifications/email-config/test/', views.email_test, name='email-test'),
    path('', include(router.urls)),
]
