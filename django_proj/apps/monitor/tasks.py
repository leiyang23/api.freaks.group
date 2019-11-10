import requests
import redis

from celery import shared_task
from django.conf import settings


@shared_task(ignore_result=True)
def heartbeat(host, port=80):
    """网站心跳监控"""
    r = redis.Redis(host=settings.REDIS_HOST, db=9)
    r.sadd("hosts", host)

    try:
        res = requests.get(f'http://{host}:{port}/heartbeat')
    except Exception as e:
        r.lpush(host, 0)
    else:
        if res.status_code == 200:
            r.lpush(host, 1)
        else:
            r.lpush(host, 0)
    finally:

        if r.llen(host) > 10:
            r.brpop([host])
        r.close()
