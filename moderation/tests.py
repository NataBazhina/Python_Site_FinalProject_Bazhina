import pytest
from django.contrib.auth import get_user_model
from ads.models import Ad
from moderation.models import ModerationRecord

User = get_user_model()


@pytest.mark.django_db
def test_moderation_record_creation():
    user = User.objects.create(username="testuser", password="testpass")
    moderator = User.objects.create(username="moderator", password="modpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status="pending",
    )
    record = ModerationRecord.objects.create(
        ad=ad,
        status="published",
        reason="Approved by moderator",
        moderator=moderator,
    )
    assert record.ad == ad
    assert record.status == "published"
    assert record.reason == "Approved by moderator"
    assert record.moderator == moderator


@pytest.mark.django_db
def test_moderation_record_optional_fields():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status="pending",
    )
    record = ModerationRecord.objects.create(
        ad=ad,
        status="published",
    )
    assert record.reason == ""
    assert record.moderator is None


@pytest.mark.django_db
def test_moderation_record_str_method():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status="pending",
    )
    record = ModerationRecord.objects.create(
        ad=ad,
        status="published",
        reason="Approved by moderator",
    )
    assert str(record) == "Test Ad: published"
