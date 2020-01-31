from django.views import View
from django.http import JsonResponse

from .models import WeatherTipList
from user.decorators import auth_permission_required


# Create your views here.

class WeatherTipView(View):
    @staticmethod
    @auth_permission_required("user.select_user")
    def get(req):
        res = WeatherTipList.objects.filter(user__username=req.username)
        return JsonResponse({
            "status_code": 200,
            "msg": "success",
            "data": list(res.values())
        })

    @staticmethod
    @auth_permission_required("user.select_user")
    def post(req):
        try:
            email = req.POST.get("email", None)
            address = req.POST.get("address", None)
            username = req.username

            tip = WeatherTipList.objects.create(email=email, address=address, user_id=username)

            return JsonResponse({
                "status_code": 200,
                "msg": "success",
                "id": tip.id
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status_code": 500,
                "msg": "fail",
            })

    @staticmethod
    @auth_permission_required("user.select_user")
    def delete(req):
        try:
            username = req.username
            tip_ids = req.GET.get("tip_ids", None)
            tip_ids = tip_ids.split("-")[:-1] if tip_ids.endswith("-") else tip_ids
            res = WeatherTipList.objects.filter(user_id=username, id__in=tip_ids).delete()
            return JsonResponse({
                "status_code": 200,
                "msg": f"success delete {res[0]} 条数据",
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status_code": 400,
                "msg": "fail"
            })
