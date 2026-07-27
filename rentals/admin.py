from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("ad", "renter", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "start_date", "end_date", "created_at")
    search_fields = ("ad__title", "renter__username")
