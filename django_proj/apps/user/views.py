import redis
import random

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegisterUserForm, LoginUserForm, RegisterEmailForm, RetrieveForm
from celery_proj.tasks.common import send_email
from .decorators import auth_permission_required
from .models import SysRemind

UserModel = get_user_model()


def register_email_code(request):
    """注册时发送邮箱激活码"""
    form = RegisterEmailForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_text()
        })
    email = form.cleaned_data['email']

    # 异步发送邮箱验证码
    subject = "邮箱验证"
    code = ''.join(random.choices('0123456789', k=4))
    message = f"激活码：{code}，15分钟内有效。"
    send_email.delay([email], subject, message)

    r = redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9)
    r.set(email, code, ex=60 * 15)

    return JsonResponse({
        "status_code": 200,
        "msg": "已发送，请查收"
    })


@require_http_methods(["POST", "OPTIONS"])
def register(request):
    """注册"""
    form = RegisterUserForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })

    password = make_password(form.cleaned_data['password'])
    email = form.cleaned_data['email']
    code = form.cleaned_data['code']

    r = redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9)
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

    user = UserModel.objects.create(password=password, email=email, msg_num=1)

    # 赋予查看默认权限
    content_type = ContentType.objects.get_for_model(UserModel)
    permission = Permission.objects.get(codename="select_user", content_type=content_type)
    user.user_permissions.add(permission)

    SysRemind.objects.create(title="欢迎新伙伴", content="欢迎加入我们，这是测试内容", status=0, user_id=user.pk)
    return JsonResponse({
        "status_code": 200,
        "msg": "register succeed",
        "token": user.token,
        "msg_num": 1
    })


@require_http_methods(['POST', 'OPTIONS'])
def login(request):
    """登陆"""
    form = LoginUserForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "status_code": 400,
            "msg": form.errors.as_json()
        })

    account = form.cleaned_data['account']
    password = form.cleaned_data['password']
    try:
        user = UserModel.objects.get(Q(username=account) | Q(email=account))
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
        "token": user.token,
        "msg_num": user.msg_num
    })


@require_http_methods(["POST", "OPTIONS"])
@auth_permission_required("select_user")
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

    send_email.delay(email)
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

    r = redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9)
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


@auth_permission_required("user.select_user")
def get_info(req):
    username = req.username
    res = list(UserModel.objects.filter(username=username).values())[0]
    del res["password"]

    return JsonResponse({
        "status_code": 200,
        "data": res
    })


@auth_permission_required("user.select_user")
def get_msgs(req):
    user = req.username
    res = list(SysRemind.objects.filter(user__username=user, status=0).values())
    return JsonResponse({
        "code": 200,
        "data": res,
        "msg_num": len(res)
    })


@auth_permission_required("user.select_user")
def del_msg(req, msg_id):
    msg = SysRemind.objects.filter(pk=msg_id)
    if len(msg) == 1:
        user = UserModel.objects.get(username=req.username)
        user.msg_num -= 1
        user.save()

        return JsonResponse({
            "code": 200,
            "msg": "delete success"
        })
    else:
        return JsonResponse({
            "code": 400,
            "msg": f"not found msg_id {msg_id}"
        })


@auth_permission_required("user.select_user")
def read_msg(req, msg_id):
    try:
        msg = SysRemind.objects.get(pk=msg_id)
        msg.status = 1
        msg.save()

        user = UserModel.objects.get(username=req.username)
        user.msg_num -= 1
        user.save()

        return JsonResponse({
            "code": 200,
            "msg": "update status"
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": 400,
            "msg": f"{msg_id} or {req.username} doesn't exist"
        })

