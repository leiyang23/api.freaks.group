import requests
import redis
import base64

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

# 百度云应用：文字审核文字识别
AK = "AX2Q6snV420igZxsWB3lz5wj"
SK = "UWBPdP775VcqFa1MyNZN2jy9K5Fi6EUR"


def get_access_token():
    with redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9) as redis_client:
        res = redis_client.get("baidu_access_token")
        if res:
            return res
        else:
            host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
            try:
                response = requests.get(host, timeout=10).json()
                access_token = response['access_token']
                redis_client.set("baidu_access_token", access_token, ex=int(response['expires_in']) - 10)
                return access_token

            except (AttributeError, TimeoutError):
                print("百度云 获取 access token api 异常")
                return None
            except KeyError:
                print("认证参数有误")
                return None


@require_POST
def text_verity(req):
    """文本审核"""
    text = req.POST.get("text", None)
    if not text:
        return JsonResponse({
            "errcode": -1,
            "msg": "内容不能为空"
        })

    if len(text) >= 20000:
        text = text[:20000]

    if not isinstance(text, str):
        text = str(text).encode("utf8").decode("utf8")

    access_token = get_access_token()
    if not access_token:
        return JsonResponse({
            "errcode": -1,
            "msg": "网络异常：不能获取token"
        })

    host = f"https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token={access_token}"
    data = {
        "content": text
    }

    res = requests.post(host, data=data)
    return JsonResponse({
        "errcode": 0,
        "msg": "success",
        "data": res.json()
    })


@require_POST
def ocr(req):
    image = req.FILES.get("image", None)
    url = req.POST.get("url", None)

    if not image and not url:
        return JsonResponse({
            "errcode": -1,
            "msg": "空数据"
        })

    if image:
        con = b""
        for d in image.chunks():
            con += d
        i = base64.b64encode(con)
        data = {
            "image": i
        }
    else:
        if url.startswith("https"):
            return JsonResponse({
                "errcode": -1,
                "msg": "不支持 https 的图片地址"
            })
        data = {
            "url": url
        }

    access_token = get_access_token()
    if not access_token:
        return JsonResponse({
            "errcode": -1,
            "msg": "网络异常：不能获取token"
        })

    # 使用 redis 来记录 接口调用量
    with redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9,
                     decode_responses=True) as redis_client:
        if redis_client.exists("ocr_type") == 0:
            num = {
                "general_basic": 5000,
                "webimage": 500,
                "accurate_basic": 500
            }
            redis_client.hmset("ocr_type", num)
        # 获取接口调用量
        remanent_times = redis_client.hgetall("ocr_type")
        if int(remanent_times['webimage']) > 0:
            ocr_type = "webimage"
        elif int(remanent_times['accurate_basic']) > 0:
            ocr_type = "accurate_basic"
        elif int(remanent_times['general_basic']) > 0:
            ocr_type = "general_basic"
        else:
            return JsonResponse({
                "errcode": -1,
                "msg": "今日次数已用尽，请明天再试"
            })

        host = f"https://aip.baidubce.com/rest/2.0/ocr/v1/{ocr_type}?access_token={access_token}"

        res = requests.post(host, data=data).json()

        redis_client.hset("ocr_type", ocr_type, int(remanent_times[ocr_type]) - 1)

        if "error_code" in res:
            msg = "网络错误，请稍后再试"
            if res['error_code'] == 18:
                msg = "QPS 太高，请稍后再试"

            return JsonResponse({
                "errcode": -1,
                "msg": msg
            })

        return JsonResponse({
            "errcode": 0,
            "data": res
        })
