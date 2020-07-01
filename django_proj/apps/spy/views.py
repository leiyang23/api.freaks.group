import json
import platform

import redis
from django.http import JsonResponse
from django.shortcuts import render

from spy.setting import SPY_REDIS


# Create your views here.
def index(req):
    return render(req, 'spy/index.html')


def base(req):
    redis_client = redis.Redis(host=SPY_REDIS.host, password=SPY_REDIS.password, db=SPY_REDIS.db)
    data = redis_client.get(platform.node() + "-base")
    redis_client.close()

    return JsonResponse({
        "errcode": 0,
        "msg": "",
        "data": json.loads(data)
    })
