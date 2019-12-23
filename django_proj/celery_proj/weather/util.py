import requests

from celery_proj.weather.setting import KEY
from celery_proj.settings import logger


def tomorrow_weather(address: str):
    """返回明天天气"""
    res, adcode = get_adcode(address)
    if not res:
        info = f"地址格式有误，无法解析：{adcode}"
        logger.error(info)
        raise ValueError(info)

    api = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": KEY,
        "extensions": 'all',
        "city": adcode
    }

    res = requests.get(api, params=params, timeout=30)
    if res.status_code != 200:
        info = "天气接口异常"
        logger.error(info)
        raise ValueError(info)

    data = res.json()
    logger.debug(data)
    if data['status'] != "1":
        info = f"无法获取天气：{data['info']}"
        logger.error(info)
        raise ValueError(info)

    casts = data["forecasts"][0]['casts']

    temp_change = int(casts[1]['daytemp']) - int(casts[0]['daytemp'])
    weather = casts[1]['dayweather']
    logger.debug(weather)

    return weather,temp_change


def get_adcode(address: "结构化地址信息"):
    """根据用户填写的地址解析出对应的 adcode"""
    api = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": KEY,
        "address": address,
    }
    res = requests.get(api, params=params, timeout=30)
    if res.status_code != 200:
        raise ValueError("地址转 adcode 接口异常")

    data = res.json()
    logger.debug(data)
    if data['status'] != "1":
        logger.error(data['info'])
        return False, data['info']

    return True, data['geocodes'][0]["adcode"]
