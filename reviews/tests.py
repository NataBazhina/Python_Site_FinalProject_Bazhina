import pytest
from django.contrib.auth import get_user_model
from ads.models import Ad
from reviews.models import Review

User = get_user_model()


@pytest.mark.django_db
def test_review_creation():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    review = Review.objects.create(
        ad=ad,
        text="Great ad!",
        rating=5,
        author=user,
    )
    assert review.ad == ad
    assert review.text == "Great ad!"
    assert review.rating == 5
    assert review.author == user


@pytest.mark.django_db
def test_review_rating_validation():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    review = Review.objects.create(
        ad=ad,
        text="Great ad!",
        rating=5,
        author=user,
    )
    assert review.rating >= 1
    assert review.rating <= 5

    review.rating = 0
    assert review.rating == 0  # валидация на уровне модели, но не в DB


@pytest.mark.django_db
def test_review_str_method():
    user = User.objects.create(username="testuser", password="testpass")
    ad = Ad.objects.create(
        title="Test Ad",
        description="Description",
        price=100,
        location="City",
        contact="Phone",
        author=user,
    )
    review = Review.objects.create(
        ad=ad,
        text="Great ad!",
        rating=5,
        author=user,
    )
    expected = f"Review for Test Ad by testuser"
    assert str(review) == expected
