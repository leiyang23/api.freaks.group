import json
import platform
from datetime import datetime

import redis
from apscheduler.schedulers.background import BackgroundScheduler

from spy.setting import SPY_REDIS
from spy.agent.aggregate import base, realtime


def collection_base_info(redis_client=None):
    data = base()
    key = platform.node() + "-base"
    redis_client.set(key, json.dumps(data))


def collection_realtime_info(redis_client=None):
    data = realtime(5)
    key = platform.node() + "-realtime"

    res = redis_client.lpush(key, json.dumps(data))
    if res > 10:
        redis_client.ltrim(key, 0, 9)


def start_agent():
    scheduler = BackgroundScheduler()
    redis_client = redis.Redis(host=SPY_REDIS.host, password=SPY_REDIS.password, db=SPY_REDIS.db, encoding="utf8")

    scheduler.add_job(collection_base_info, 'interval', hours=3,
                      id="base_info",
                      kwargs={"redis_client": redis_client},
                      next_run_time=datetime.now())
    scheduler.add_job(collection_realtime_info, 'interval', seconds=10,
                      id="realtime_info",
                      kwargs={"redis_client": redis_client},
                      next_run_time=datetime.now())
    scheduler.start()


if __name__ == '__main__':
    pass
