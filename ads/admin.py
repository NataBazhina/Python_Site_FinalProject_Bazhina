from django.contrib import admin
from ads.models import Ad
from moderation.models import ModerationRecord


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "description", "location", "contact")
    actions = ["approve_ads", "reject_ads"]

    def approve_ads(self, request, queryset):
        for ad in queryset:
            ad.status = Ad.Status.PUBLISHED
            ad.save()

            ModerationRecord.objects.create(
                ad=ad,
                status=ModerationRecord.Status.PUBLISHED,
                reason="Approved by moderator",
                moderator=request.user,
            )

    approve_ads.short_description = "Approve selected ads"

    def reject_ads(self, request, queryset):
        for ad in queryset:
            ad.status = Ad.Status.REJECTED
            ad.save()

            ModerationRecord.objects.create(
                ad=ad,
                status=ModerationRecord.Status.REJECTED,
                reason="Rejected by moderator",
                moderator=request.user,
            )

    reject_ads.short_description = "Reject selected ads"
