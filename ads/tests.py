import pytest
from django.contrib.auth import get_user_model
from ads.models import Ad

User = get_user_model()


@pytest.mark.django_db
def test_ad_creation():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status="draft",
    )
    assert ad.title == "Test Ad"
    assert ad.price >= 0
    assert ad.status == "draft"

    def __str__(self):
        return self.title


@pytest.mark.django_db
def test_ad_status_transition():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
        status="draft",
    )
    assert ad.status == "draft"


@pytest.mark.django_db
def test_ad_str_method():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    assert str(ad) == "Test Ad"


@pytest.mark.django_db
def test_ad_price_validation():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    assert ad.is_valid_price() == True

    ad.price = -10
    assert ad.is_valid_price() == False
