import redis
import random

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import RegisterUserForm, LoginUserForm, RegisterEmailForm, RetrieveForm
from celery_proj.tasks.common import send_email

UserModel = get_user_model()


@require_POST
def register_email_code(request):
    """注册时发送邮箱激活码"""
    form = RegisterEmailForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })
    email = form.cleaned_data['email']

    # 异步发送邮箱验证码
    subject = "邮箱验证"
    code = ''.join(random.choices('0123456789', k=4))
    message = f"激活码：{code}，15分钟内有效。"
    send_email.delay([email],subject,message)

    r = redis.Redis(host=settings.REDIS_HOST, db=9)
    r.set(email, code, ex=60 * 15)

    return JsonResponse({
        "status_code": 200,
        "msg": "已发送，请查收"
    })


@require_POST
def register(request):
    """注册"""
    form = RegisterUserForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })

    username = form.cleaned_data['username']
    password = make_password(form.cleaned_data['password'])
    email = form.cleaned_data['email']
    code = form.cleaned_data['code']

    r = redis.Redis(host=settings.REDIS_HOST, db=9)
    active_code = r.get(email)

    if active_code is None:
        return JsonResponse({
            "status_code": 400,
            "msg": "邮箱不正确或验证码已过期"
        })
    if code != active_code.decode():
        return JsonResponse({
            "status_code": 400,
            "msg": "验证码不正确"
        })
    r.delete(email)

    user = UserModel.objects.create(username=username, password=password, email=email)
    return JsonResponse({
        "status_code": 200,
        "msg": "register succeed",
        "token": user.token
    })


@require_POST
def login(request):
    """登陆"""
    form = LoginUserForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    try:
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        return JsonResponse({
            "status_code": 400,
            "msg": "用户不存在"
        })

    if not check_password(password, user.password):
        return JsonResponse({
            "status_code": 400,
            "msg": "用户密码不正确"
        })
    return JsonResponse({
        "status_code": 200,
        "msg": "login succeed",
        "token": user.token
    })


@require_POST
def retrieve_verify_email(request):
    """找回密码时验证邮箱"""
    email = request.POST.get("email", None)
    try:
        UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return JsonResponse({
            "status_code": 400,
            "msg": "邮箱不存在"
        })

    send_active_email.delay(email)
    return JsonResponse({
        "status_code": 200,
        "msg": "已发送，请查收"
    })


@require_POST
def retrieve(request):
    """找回密码/重设密码"""
    form = RetrieveForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    code = form.cleaned_data['code']

    r = redis.Redis(host=settings.REDIS_HOST, db=9)
    active_code = r.get(email)

    if active_code is None:
        return JsonResponse({
            "status_code": 400,
            "msg": "邮箱不正确或验证码已过期"
        })
    if code != active_code.decode():
        return JsonResponse({
            "status_code": 400,
            "msg": "验证码不正确"
        })
    r.delete(email)

    user = UserModel.objects.get(email=email)
    user.password = make_password(password)
    user.save()
    return JsonResponse({
        "status_code": 200,
        "msg": "retrieve succeed",
        "token": user.token
    })
