from django.urls import path
from .views import ocr, text_verity

urlpatterns = [
    path(r"text_verify", text_verity),
    path(r"ocr", ocr),
]
