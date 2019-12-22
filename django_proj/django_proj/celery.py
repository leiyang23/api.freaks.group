import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_proj.settings')

app = Celery('django_proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# 定时任务
app.conf.beat_schedule = {
    'monitor-local-site': {
        'task': 'monitor.tasks.heartbeat',
        'schedule': 60.0 * 6,
        'args': ("localhost",),
        'kwargs': {'port': 9000}
    },
    'monitor-site': {
        'task': 'monitor.tasks.heartbeat',
        'schedule': 60.0 * 6,
        'args': ("api.freaks.group",),
        'kwargs': {'port': 80}
    },
    'reset-baidu-api-times': {
        "task": 'ai.tasks.reset_api_times',
        "schedule": crontab(hour=0, minute=0)
    }
}
