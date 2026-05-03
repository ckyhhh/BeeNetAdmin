"""系统设置 URL"""
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('system/settings/', views.system_settings, name='system-settings'),
    path('system/auto-backup/', views.auto_backup, name='auto-backup'),
    path('system/backup/', views.backup_now, name='backup-now'),
    path('system/templates/textfsm/', views.textfsm_templates, name='textfsm-templates'),
    path('system/templates/jinja2/', views.jinja2_templates, name='jinja2-templates'),
]
