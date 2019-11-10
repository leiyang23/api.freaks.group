from django.urls import path

from . import views


urlpatterns = [
    path('site_monitor',views.site_monitor),
]