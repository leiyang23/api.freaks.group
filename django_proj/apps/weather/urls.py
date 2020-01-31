from django.urls import path
from . import views

urlpatterns = [
    path("weather_tip", views.WeatherTipView.as_view()),
]
