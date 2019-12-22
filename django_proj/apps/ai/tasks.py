import redis

from celery import shared_task
from django.conf import settings


@shared_task(ignore_result=True)
def reset_api_times():
    with redis.Redis(host=settings.REDIS_HOST, db=9) as redis_client:
        redis_client.delete("ocr_type")
