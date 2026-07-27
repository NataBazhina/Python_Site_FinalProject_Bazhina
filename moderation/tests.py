import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad
from moderation.models import ModerationRecord

User = get_user_model()


@pytest.mark.django_db
def test_moderation_record_creation():
    user = User.objects.create_user(username="testuser", password="testpass")
    moderator = User.objects.create_user(username="moderator", password="modpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
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
def test_moderation_record_optional_fields():
    user = User.objects.create_user(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status=Ad.Status.PENDING,
    )
    record = ModerationRecord.objects.create(
        ad=ad,
        status=ModerationRecord.Status.PUBLISHED,
    )
    assert record.reason == ""
    assert record.moderator is None


@pytest.mark.django_db
def test_moderation_record_str_method():
    user = User.objects.create_user(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status=Ad.Status.PENDING,
    )
    record = ModerationRecord.objects.create(
        ad=ad,
        status=ModerationRecord.Status.PUBLISHED,
        reason="Approved by moderator",
    )
    assert str(record) == "Test Ad: published"


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
    )


@pytest.mark.django_db
def test_new_ad_is_pending_by_default(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "Moderation ad",
        "description": "Needs moderation",
        "price": "100.00",
        "location": "Moscow",
        "contact": "owner@example.com",
    }

    client.post(url, data)

    ad = Ad.objects.get(title="Moderation ad")
    assert ad.status == Ad.Status.PENDING


@pytest.mark.django_db
def test_pending_ads_not_visible_on_home(client, user):
    Ad.objects.create(
        title="Pending ad",
        description="Pending",
        price="100.00",
        location="Moscow",
        contact="test@example.com",
        author=user,
        status=Ad.Status.PENDING,
    )

    response = client.get(reverse("home"))
    content = response.content.decode(response.charset)
    assert "Pending ad" not in content


@pytest.mark.django_db
def test_published_ads_visible_on_home(client, user):
    Ad.objects.create(
        title="Published ad",
        description="Published",
        price="100.00",
        location="Moscow",
        contact="test@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    response = client.get(reverse("home"))
    content = response.content.decode(response.charset)
    assert "Published ad" in content