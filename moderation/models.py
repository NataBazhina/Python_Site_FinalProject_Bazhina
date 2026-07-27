from django.conf import settings
from django.db import models


class ModerationRecord(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"
        ARCHIVED = "archived", "Archived"

    ad = models.ForeignKey(
        "ads.Ad",
        on_delete=models.CASCADE,
        related_name="moderation_records",
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    reason = models.TextField(blank=True)
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderation_actions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ad.title}: {self.status}"
