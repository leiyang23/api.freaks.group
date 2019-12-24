from celery_proj.app import app
from celery_proj.settings import logger
from celery_proj.tasks.common import send_email

from celery_proj.weather.util import tomorrow_weather
from celery_proj.weather.setting import SAFE_WEATHER,USERS


@app.task
def weather():
    for user in USERS:
        weather, temp_change = tomorrow_weather(user['address'])
        logger.debug(weather, temp_change)
        if weather not in SAFE_WEATHER or abs(temp_change) >= 5:
            send_email.apply_async(([user['email']], weather+ "\n温差：" + str(temp_change)))