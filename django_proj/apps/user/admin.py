from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ("头像", {'fields': ('avatar', )})
    )


admin.site.site_header = "网站后台管理"
admin.site.site_title = "个人网站"
