import redis

from django.conf import settings
from django.http import JsonResponse


# Create your views here.
def site_monitor(req):
    res = []
    r = redis.Redis(settings.REDIS_HOST, db=9)
    hosts = r.smembers("hosts")

    for host in hosts:
        item = {
            "name": host.decode(),
            "ping_res": [i.decode() for i in r.lrange(host, 0, 9)]
        }
        res.append(item)
    r.close()
    return JsonResponse({
        "status_code": 200,
        "data": res
    })
