from django.forms import ModelForm
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import User

username_validator = UnicodeUsernameValidator()


class RegisterEmailForm(ModelForm):
    """注册邮箱"""

    class Meta:
        model = User
        fields = ["email"]


class RegisterUserForm(ModelForm):
    """注册"""
    code = forms.CharField(max_length=4, min_length=4, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]


class LoginUserForm(ModelForm):
    """登陆"""
    username = forms.CharField(max_length=150, validators=[username_validator])

    class Meta:
        model = User
        fields = ["password"]


class RetrieveForm(ModelForm):
    """重设密码"""
    email = forms.EmailField(required=True)
    code = forms.CharField(max_length=4, min_length=4, required=True)

    class Meta:
        model = User
        fields = ["password"]
