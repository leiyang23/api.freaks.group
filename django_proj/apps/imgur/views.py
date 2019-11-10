import requests
from qiniu import Auth
import datetime

from django.http import JsonResponse


# Create your views here.
def get_token(name):
    """返回七牛云上传token"""

    access_key = 'ifQf2JhtpIsK354ZT69bKbMtBPsDzNlQNizohXHm'
    secret_key = 'GxBrXLvPiMxls5cqdOdorlwtBW42OulonwMsIHFd'
    q = Auth(access_key, secret_key)

    bucket_name = 'test'

    key = name
    # 生成上传 Token，可以指定过期时间等
    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200'
    }
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name, key, 3600, policy)
    return token


def up_tokens(request):
    """批量返回tokens"""
    file_name_str = request.GET.get("file_name_str", None)
    if file_name_str is None:
        return JsonResponse({
            "status_code": 400,
            "msg": "必须带文件名"
        })
    # file_name_str 形如：a.jpg@@b.png@@
    file_name_list = [name for name in file_name_str.split("@@")[:-1]]
    tokens = []
    for file_name in file_name_list:
        tokens.append(get_token(file_name))
    return JsonResponse({
        "status_code": 200,
        "data": tokens
    })


def qiniu_data_statistic(request):
    """七牛云接口统计"""

    res = {
        "space": 0,
        "count": 0
    }
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S")
    access_key = 'ifQf2JhtpIsK354ZT69bKbMtBPsDzNlQNizohXHm'
    secret_key = 'GxBrXLvPiMxls5cqdOdorlwtBW42OulonwMsIHFd'
    q = Auth(access_key, secret_key)

    for i in res:
        url = f'http://api.qiniu.com/v6/{i}?bucket=test&begin={yesterday}&end={today}&g=day'
        access_token = q.token_of_request(url=url) # 管理凭证

        headers = {
            "Authorization": "QBox " + access_token
        }

        resp = requests.get(url, headers=headers).json()
        res[i] = resp['datas'][-1]
    return JsonResponse({
        "status_code": 200,
        "data": res
    })
