"""
BeeAdmin URL 配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.devices.urls')),
    path('api/v1/', include('apps.scanning.urls')),
    path('api/v1/', include('apps.inspection.urls')),
    path('api/v1/', include('apps.alive.urls')),
    path('api/v1/', include('apps.terminal.urls')),
    path('api/v1/', include('apps.notification.urls')),
    path('api/v1/', include('apps.ai.urls')),
    path('api/v1/', include('apps.system.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
