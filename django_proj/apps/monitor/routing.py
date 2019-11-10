from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/monitor/get_host_info', consumers.MonitorHostConsumer),
    re_path(r'ws/monitor/terminal', consumers.TerminalConsumer),
]