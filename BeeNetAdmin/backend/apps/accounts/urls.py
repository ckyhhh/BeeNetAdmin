"""用户认证 URL"""
from django.urls import path
from . import views

urlpatterns = [
    path('setup/status/', views.setup_status, name='setup-status'),
    path('setup/', views.setup_view, name='setup'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/me/', views.me_view, name='me'),
    path('auth/password/', views.change_password, name='change-password'),
    path('auth/unlock/', views.unlock_view, name='unlock'),
    path('auth/lock/', views.lock_view, name='lock'),
]
