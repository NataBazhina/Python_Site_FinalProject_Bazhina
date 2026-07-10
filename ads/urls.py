from django.urls import path
from . import views
from .views import AdCreateView, AdDetailView, AdUpdateView

app_name = "ads"

urlpatterns = [
    path("", views.ad_list, name="home"),
    path("create/", AdCreateView.as_view(), name="create"),
    path("<int:pk>/", AdDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="edit"),
]