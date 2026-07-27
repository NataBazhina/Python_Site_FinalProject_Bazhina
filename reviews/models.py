from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    ad = models.ForeignKey(
        "ads.Ad",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review for {self.ad.title} by {self.author}"
