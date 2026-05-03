"""终端 WebSocket Consumer"""
import json
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone


class SSHTerminalConsumer(WebsocketConsumer):
    """SSH 终端 WebSocket"""

    def connect(self):
        self.device_id = self.scope['url_route']['kwargs'].get('device_id')
        self.accept()
        self.send(text_data=json.dumps({'type': 'connected', 'message': '已连接'}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', '')

        if msg_type == 'command':
            # TODO: 通过 SSH 连接执行命令并返回输出
            self.send(text_data=json.dumps({
                'type': 'output',
                'data': f'Echo: {data.get("command", "")}\n'
            }))


class TelnetTerminalConsumer(WebsocketConsumer):
    """Telnet 终端 WebSocket"""

    def connect(self):
        self.device_id = self.scope['url_route']['kwargs'].get('device_id')
        self.accept()
        self.send(text_data=json.dumps({'type': 'connected', 'message': '已连接'}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', '')

        if msg_type == 'command':
            self.send(text_data=json.dumps({
                'type': 'output',
                'data': f'Echo: {data.get("command", "")}\n'
            }))
