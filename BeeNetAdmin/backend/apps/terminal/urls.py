"""终端 URL"""
from django.urls import path
from . import views

urlpatterns = [
    path('terminal/instant/history/', views.instant_history, name='instant-history'),
    path('terminal/instant/history/<int:pk>/', views.instant_delete, name='instant-delete'),
    path('terminal/instant/<int:pk>/log/', views.instant_log, name='instant-log'),
]
