import os
import json
import time
import platform

from channels.generic.websocket import WebsocketConsumer

from .utils import monitor_info


class MonitorHostConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=json.dumps({
            'message': monitor_info()
        }))

    def disconnect(self, close_code):
        pass


class TerminalConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': f"当前操作系统：{platform.system()}"
        }))

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print("前台的指令：" + message)
        for line in os.popen(message, buffering=1):
            self.send(text_data=json.dumps({
                'message': line
            }))
