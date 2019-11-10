import random
import redis

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_active_email(email):
    subject = "邮箱验证"
    code = ''.join(random.choices('0123456789', k=4))
    message = f"激活码：{code}，15分钟内有效。"

    r = redis.Redis(host=settings.REDIS_HOST, db=9)
    r.set(email, code, ex=60 * 15)

    send_mail(subject, message, 'leiyang_ace@163.com', [email])
