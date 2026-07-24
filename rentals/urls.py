from django.urls import path
from . import views

app_name = "rentals"

urlpatterns = [
    path("<int:pk>/create/", views.create_rental, name="create"),
    path("my/", views.my_rentals, name="my_rentals"),
    path("<int:rental_id>/review/", views.add_review, name="add_review"),
]
