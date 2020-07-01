from collections import namedtuple

from django.conf import settings


spy_redis = namedtuple("SPY_REDIS", "host, port, password, db", defaults=[12])

if hasattr(settings, "SPY_REDIS") and isinstance(settings.SPY_REDIS, dict):
    SPY_REDIS = spy_redis(**settings.SPY_REDIS)
else:
    raise ValueError("please provide `SPY_REDIS` in settings.py")
