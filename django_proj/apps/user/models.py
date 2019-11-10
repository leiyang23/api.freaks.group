import jwt
import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

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
        default_permissions = ()

        permissions = (
            ("select_user", "查看用户"),
            ("change_user", "修改用户"),
            ("delete_user", "删除用户"),
        )
