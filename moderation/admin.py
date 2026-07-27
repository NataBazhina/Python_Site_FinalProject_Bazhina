from django.contrib import admin
from moderation.models import ModerationRecord
from ads.models import Ad


@admin.register(ModerationRecord)
class ModerationRecordAdmin(admin.ModelAdmin):
    list_display = ("ad", "status", "moderator", "created_at")
    list_filter = ("status", "created_at", "moderator")
    search_fields = ("ad__title", "reason", "moderator__username")
    readonly_fields = ("ad", "status", "reason", "moderator", "created_at")
