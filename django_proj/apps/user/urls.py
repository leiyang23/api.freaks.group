from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register),
    path("login", views.login),
    path("retrieve", views.retrieve),
    path("register_email_code", views.register_email_code),
    path("retrieve_verify_email", views.retrieve_verify_email),

    path("info", views.get_info),
]
