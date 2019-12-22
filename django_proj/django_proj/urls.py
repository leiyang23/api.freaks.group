from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def heartbeat(request):
    """本站的监控"""
    return HttpResponse("ok")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('heartbeat', heartbeat),
    path('account/', include('user.urls')),
    path('imgur/', include('imgur.urls')),
    path('monitor/', include('monitor.urls')),
    path('ai/', include('ai.urls')),
]
