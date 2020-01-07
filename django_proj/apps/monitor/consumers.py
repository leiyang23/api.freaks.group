import traceback
import json


from channels.generic.websocket import WebsocketConsumer

from .utils import monitor_info, SSH


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
            'message': "已连接到后端服务器\n",
        }))

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        try:
            message = text_data_json['message']
            if not hasattr(self, "ssh") or not hasattr(self, "shell"):
                # 第一次连接
                ssh = SSH(**text_data_json['conn_info'])
                shell = ssh.get_shell()
                self.__dict__.update({"ssh": ssh})
                self.__dict__.update({"shell": shell})

                self.send(text_data=json.dumps({
                    "message": "已连接到远程服务器！",
                    "status": "ok"
                }))
            else:
                resp = self.ssh.cmd(self.shell, message)
                self.send(text_data=json.dumps({
                    "message": resp
                }))

        except ConnectionError:
            traceback.print_exc()
            self.send(text_data=json.dumps({
                "message": "连接错误，请核对连接信息！",
                "status": "bad"
            }))

        except KeyError:
            traceback.print_exc()
            self.send(text_data=json.dumps({
                "message": "消息格式错误，"
            }))
