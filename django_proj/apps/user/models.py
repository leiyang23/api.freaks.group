import jwt
import time
import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

import requests


def _gen_username():
    return "user" + str(int(time.time()))


def _gen_avatar():
    try:
        res = requests.get("http://api.btstu.cn/sjtx/api.php?lx=c1&format=json", timeout=10).json()
        if res['code'] == "200":
            image_url = res['imgurl']
        else:
            raise ValueError
    except:
        image_url = "http://qiniu1.freaks.group/37a984d01ed02791b77f8b922066c017.jpg"

    return image_url


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, default=_gen_username, verbose_name="用户名")
    email = models.EmailField(unique=True, verbose_name="邮箱")

    gender = models.SmallIntegerField(verbose_name="性别", default=0, choices=((0, "未知"), (1, "男"), (2, "女")))
    avatar = models.URLField(verbose_name="头像地址", default=_gen_avatar)

    msg_num = models.SmallIntegerField("未读消息", default=0)

    @property
    def token(self):
        return self._generate_token()

    def _generate_token(self):
        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(),
            "data": {
                "username": self.username
            }
        }
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token.decode("utf-8")

    class Meta:
        verbose_name = "成员"
        verbose_name_plural = verbose_name
        default_permissions = ()

        permissions = (
            ("select_user", "查看用户"),
            ("change_user", "修改用户"),
            ("delete_user", "删除用户"),
        )


class SysMessage(models.Model):
    """ 系统（全员）消息 """
    title = models.CharField("标题", max_length=100)
    content = models.TextField("消息内容", )

    status = models.SmallIntegerField("消息状态", choices=((0, "未读"), (1, "已读"), (2, "已删除"), (3, "已撤销")))
    create_time = models.DateTimeField("发布时间", auto_now_add=True)

    user = models.ManyToManyField(User, )


class SysRemind(models.Model):
    """ 私人提醒 """
    title = models.CharField("标题", max_length=100)
    content = models.TextField("消息内容", )

    status = models.SmallIntegerField("消息状态", choices=((0, "未读"), (1, "已读"), (2, "已删除"), (3, "已撤销")))
    create_time = models.DateTimeField("发布时间", auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
