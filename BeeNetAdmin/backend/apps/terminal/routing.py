"""终端 WebSocket 路由"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ssh/(?P<device_id>\d+)/$', consumers.SSHTerminalConsumer.as_asgi()),
    re_path(r'ws/telnet/(?P<device_id>\d+)/$', consumers.TelnetTerminalConsumer.as_asgi()),
]
