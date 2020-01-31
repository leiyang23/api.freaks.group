from celery_proj.app import app
from celery_proj.settings import logger
from celery_proj.tasks.common import send_email

from celery_proj.weather.util import tomorrow_weather
from celery_proj.weather.setting import SAFE_WEATHER, USERS


@app.task
def weather(user: dict):
    weather_desc, temp_change = tomorrow_weather(user['address'])
    logger.debug(weather_desc, temp_change)
    if weather_desc not in SAFE_WEATHER or abs(temp_change) >= 5:
        send_email.apply_async(([user['email']], "天气提醒", weather_desc + "\n温差：" + str(temp_change)))
    return user["email"]


@app.task
def main():
    import sqlite3

    conn = sqlite3.connect('db.sqlite3')
    # 创建一个cursor：
    cursor = conn.cursor()
    cursor.execute("select email, address from weather_weathertiplist")
    res = cursor.fetchall()

    for user in res:
        weather.apply_async(({"email": user[0], "address": user[1]},))

    cursor.close()
    conn.close()
