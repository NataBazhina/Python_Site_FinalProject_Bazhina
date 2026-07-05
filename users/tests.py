import pytest
from django.contrib.auth import get_user_model
from ads.models import Ad
from users.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create(username="testuser", password="testpass")
    profile = Profile.objects.create(
        user=user,
        bio="This is a bio",
        phone="1234567890",
    )
    assert profile.user == user
    assert profile.bio == "This is a bio"
    assert profile.phone == "1234567890"


@pytest.mark.django_db
def test_profile_optional_fields():
    user = User.objects.create(username="testuser", password="testpass")
    profile = Profile.objects.create(
        user=user,
    )
    assert profile.bio == ""
    assert profile.phone == ""


@pytest.mark.django_db
def test_profile_favorite_ads():
    user = User.objects.create(username="testuser", password="testpass")
    ad1 = Ad.objects.create(
        title="Ad 1",
        description="Desc 1",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    ad2 = Ad.objects.create(
        title="Ad 2",
        description="Desc 2",
        price=200,
        location="City",
        contact="Phone",
        author=user,
    )
    profile = Profile.objects.create(
        user=user,
    )
    profile.favorite_ads.add(ad1, ad2)
    assert profile.favorite_ads.count() == 2
    assert ad1 in profile.favorite_ads.all()
    assert ad2 in profile.favorite_ads.all()


@pytest.mark.django_db
def test_profile_str_method():
    user = User.objects.create(username="testuser", password="testpass")
    profile = Profile.objects.create(
        user=user,
        bio="This is a bio",
    )
    assert str(profile) == "Profile of testuser"
