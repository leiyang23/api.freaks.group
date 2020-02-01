from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def image(self, obj):
        return format_html(
            '<img src="{}" width="50px"/>',
            obj.avatar,
        )

    image.short_description = "头像"

    list_display = ('image', 'username', 'email', 'is_staff', 'gender')


admin.site.site_header = "网站后台管理"
admin.site.site_title = "个人网站"
