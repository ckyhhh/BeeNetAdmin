"""AI URL"""
from django.urls import path
from . import views

urlpatterns = [
    path('ai/config/', views.ai_config, name='ai-config'),
    path('ai/analyze/terminal/', views.ai_analyze_terminal, name='ai-analyze-terminal'),
    path('ai/chat/', views.ai_chat, name='ai-chat'),
]
