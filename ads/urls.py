from django.urls import path
from . import views
from .views import AdCreateView, AdDetailView, AdUpdateView, ad_list, AdListView, AdMyAdsView, home

app_name = "ads"

urlpatterns = [
    path("", views.ad_list, name="home"),
    path("", ad_list, name="list"),
    path("create/", AdCreateView.as_view(), name="create"),
    path("<int:pk>/", AdDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="edit"),
    path("", AdListView.as_view(), name="list"),
    path("home/", home, name="home"),
    path("my/", AdMyAdsView.as_view(), name="my"),
]