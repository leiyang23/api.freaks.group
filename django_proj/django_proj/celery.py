import os
from celery import Celery

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
}
