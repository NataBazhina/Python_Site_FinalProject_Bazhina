from django.urls import path
from . import views

app_name = "moderation"

urlpatterns = [
    path("", views.pending_ads, name="pending_ads"),
    path("<int:pk>/approve/", views.approve_ad, name="approve_ad"),
    path("<int:pk>/reject/", views.reject_ad, name="reject_ad"),
]
