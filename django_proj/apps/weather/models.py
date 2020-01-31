from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Create your models here.
class WeatherTipList(models.Model):
    mobile = models.CharField(max_length=11, default="empty", verbose_name="接受手机号")
    email = models.EmailField(verbose_name="接受邮箱")
    address = models.CharField(max_length=100, verbose_name="天气地址")

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, to_field="username", verbose_name="用户")
