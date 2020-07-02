import os
import sys
from celery import Celery
from celery.schedules import crontab
from pytz import timezone

from celery_proj import settings

proj_base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(proj_base_path, "apps"))


app = Celery('celery', broker=f"redis://:{settings.REDIS_PWD}@{settings.REDIS_HOST}:6379/9",
             backend=f"redis://:{settings.REDIS_PWD}@{settings.REDIS_HOST}:6379/9",
             include=['celery_proj.tasks.common', "celery_proj.weather.tasks"])

# 定时任务
app.conf.beat_schedule = {
    'reset-baidu-api-times': {
        "task": 'celery_proj.tasks.common.reset_api_times',
        "schedule": crontab(hour=0, minute=0)
    },
    'weather': {
        "task": 'celery_proj.weather.tasks.main',
        "schedule": crontab(minute=0, hour="20"),
    },
}
app.conf.enable_utc = False
app.conf.timezone = timezone("Asia/Shanghai")
if __name__ == '__main__':
    app.worker_main()
