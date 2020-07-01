import redis
import json
import platform
from channels.generic.websocket import WebsocketConsumer

from spy.setting import SPY_REDIS


class SpyConsumer(WebsocketConsumer):
    key = platform.node() + "-realtime"
    redis_client = redis.Redis(host=SPY_REDIS.host, password=SPY_REDIS.password, db=SPY_REDIS.db, decode_responses=True)

    def connect(self):
        self.accept()

        self.receive('{"message":"heart"}')

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "heart":
            data = self.redis_client.lindex(self.key, 0)
            self.send(text_data=data)
