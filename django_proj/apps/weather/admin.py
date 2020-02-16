from django.contrib import admin

from .models import WeatherTipList


@admin.register(WeatherTipList)
class WeatherTipListAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "address")
    list_filter = ("user",)
    search_fields = ("email", "address")
