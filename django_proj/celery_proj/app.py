from celery import Celery
from celery.schedules import crontab

from celery_proj import settings

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
        "task": 'celery_proj.weather.tasks.weather',
        "schedule": crontab(minute=0, hour="20"),
    },
}
app.conf.enable_utc = False
if __name__ == '__main__':
    app.worker_main()
