import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ads.models import Ad
from moderation.models import ModerationRecord

User = get_user_model()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def moderator(django_user_model):
    return django_user_model.objects.create_user(
        username="moderator",
        password="modpass123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def pending_ad(user):
    return Ad.objects.create(
        title="Pending ad",
        description="Pending description",
        price="100.00",
        location="Moscow",
        contact="owner@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )


@pytest.mark.django_db
def test_new_ad_is_pending_by_default(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "New moderation ad",
        "description": "Needs moderation",
        "price": "120.00",
        "location": "Moscow",
        "contact": "owner@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 302
    ad = Ad.objects.get(title="New moderation ad")
    assert ad.status == Ad.Status.PENDING
    assert ad.author == user


@pytest.mark.django_db
def test_pending_ads_not_visible_on_home(client, pending_ad):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Pending ad" not in content


@pytest.mark.django_db
def test_published_ads_visible_on_home(client, user):
    Ad.objects.create(
        title="Published ad",
        description="Published description",
        price="150.00",
        location="Moscow",
        contact="pub@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    response = client.get(reverse("home"))

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Published ad" in content


@pytest.mark.django_db
def test_admin_approve_action_creates_moderation_record(admin_client, moderator, user):
    ad = Ad.objects.create(
        title="To approve",
        description="Approve me",
        price="200.00",
        location="Moscow",
        contact="approve@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )

    url = reverse("admin:ads_ad_changelist")
    data = {
        "action": "approve_ads",
        "_selected_action": [str(ad.pk)],
        "index": 0,
    }

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    ad.refresh_from_db()
    assert ad.status == Ad.Status.PUBLISHED

    record = ModerationRecord.objects.first()
    assert record is not None
    assert record.ad == ad
    assert record.status == ModerationRecord.Status.PUBLISHED
    assert record.reason == "Approved by moderator"
    assert record.moderator.username == "admin"


@pytest.mark.django_db
def test_admin_reject_action_creates_moderation_record(admin_client, moderator, user):
    ad = Ad.objects.create(
        title="To reject",
        description="Reject me",
        price="200.00",
        location="Moscow",
        contact="reject@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )

    url = reverse("admin:ads_ad_changelist")
    data = {
        "action": "reject_ads",
        "_selected_action": [str(ad.pk)],
        "index": 0,
    }

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    ad.refresh_from_db()
    assert ad.status == Ad.Status.REJECTED

    record = ModerationRecord.objects.first()
    assert record is not None
    assert record.ad == ad
    assert record.status == ModerationRecord.Status.REJECTED
    assert record.reason == "Rejected by moderator"
    assert record.moderator.username == "admin"


@pytest.mark.django_db
def test_moderation_record_manual_creation(user, moderator):
    ad = Ad.objects.create(
        title="Manual record ad",
        description="Test",
        price="100.00",
        location="Moscow",
        contact="test@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )

    record = ModerationRecord.objects.create(
        ad=ad,
        status=ModerationRecord.Status.PUBLISHED,
        reason="Approved by moderator",
        moderator=moderator,
    )

    assert record.ad == ad
    assert record.status == ModerationRecord.Status.PUBLISHED
    assert record.reason == "Approved by moderator"
    assert record.moderator == moderator


@pytest.mark.django_db
def test_moderation_record_str_method(user, moderator):
    ad = Ad.objects.create(
        title="String ad",
        description="Test",
        price="100.00",
        location="Moscow",
        contact="test@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )

    record = ModerationRecord.objects.create(
        ad=ad,
        status=ModerationRecord.Status.PUBLISHED,
        reason="Approved by moderator",
        moderator=moderator,
    )

    assert str(record) == "String ad: published"
