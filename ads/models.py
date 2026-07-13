from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Ad(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
    )
    start_date = models.DateField(null=True, blank=True, help_text="Дата начала аренды")
    end_date = models.DateField(null=True, blank=True, help_text="Дата окончания аренды")
    image = models.ImageField(null=True, blank=True, upload_to="ads_images/", help_text="Фото объявления")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def can_submit_for_moderation(self):
        return self.status == self.Status.DRAFT

    def submit_for_moderation(self):
        if not self.can_submit_for_moderation():
            return False
        self.status = self.Status.PENDING
        self.save(update_fields=["status"])
        return True

    def publish(self):
        self.status = self.Status.PUBLISHED
        self.save(update_fields=["status"])

    def reject(self):
        self.status = self.Status.REJECTED
        self.save(update_fields=["status"])

    def archive(self):
        self.status = self.Status.ARCHIVED
        self.save(update_fields=["status"])

    def is_valid_price(self):
        return self.price >= 0
