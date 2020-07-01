import logging
from django.apps import AppConfig

from spy.agent import main

logger = logging.getLogger("custom")


class SpyConfig(AppConfig):
    name = 'spy'

    def ready(self):
        main.start_agent()
