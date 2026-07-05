from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    favorite_ads = models.ManyToManyField(
        "ads.Ad",
        blank=True,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user}"
