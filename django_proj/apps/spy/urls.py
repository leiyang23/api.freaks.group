from django.urls import path
from django.views.decorators import cache

from spy.views import base, index

urlpatterns = [
    path('index/', index),
    path('api/base', cache.cache_page(1200)(base)),
]
