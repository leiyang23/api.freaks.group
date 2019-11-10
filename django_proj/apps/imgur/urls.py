from django.urls import path

from . import views

urlpatterns = [
    path('up_tokens', views.up_tokens),
    path('qiniu_data_statistic', views.qiniu_data_statistic),
]
