from django.urls import path
from . import views
from .views import AdCreateView, AdDetailView, AdUpdateView, AdListView

app_name = "ads"

urlpatterns = [
    path("", views.home, name="home"),
    path("ads/", views.ad_list, name="list"),
    path("create/", AdCreateView.as_view(), name="create"),
    path("<int:pk>/", AdDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="edit"),
    path("my/", views.my_ads, name="my_ads"),
    path("<int:pk>/archive/", views.archive_ad, name="archive"),
]
