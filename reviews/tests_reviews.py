import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from ads.models import Ad
from reviews.forms import ReviewForm
from reviews.models import Review


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def other_user(django_user_model):
    return django_user_model.objects.create_user(
        username="otheruser",
        password="otherpass123",
    )


@pytest.fixture
def published_ad(user):
    return Ad.objects.create(
        title="Test Ad",
        description="Description",
        price="100.00",
        location="City",
        contact="Phone",
        author=user,
        status=Ad.Status.PUBLISHED,
    )


@pytest.mark.django_db
def test_review_creation(user, published_ad):
    review = Review.objects.create(
        ad=published_ad,
        text="Great ad!",
        rating=5,
        author=user,
    )

    assert review.ad == published_ad
    assert review.text == "Great ad!"
    assert review.rating == 5
    assert review.author == user


@pytest.mark.django_db
def test_review_rating_validation(user, published_ad):
    review = Review(
        ad=published_ad,
        text="Great ad!",
        rating=0,
        author=user,
    )

    with pytest.raises(ValidationError):
        review.full_clean()


@pytest.mark.django_db
def test_review_str_method(user, published_ad):
    review = Review.objects.create(
        ad=published_ad,
        text="Great ad!",
        rating=5,
        author=user,
    )

    expected = "testuser: 5/5 for Test Ad"
    assert str(review) == expected


@pytest.mark.django_db
def test_review_form_rejects_empty_text():
    form = ReviewForm(data={"text": "", "rating": 5})

    assert not form.is_valid()
    assert "text" in form.errors


@pytest.mark.django_db
def test_review_form_rejects_invalid_rating():
    form = ReviewForm(data={"text": "Nice ad", "rating": 6})

    assert not form.is_valid()
    assert "rating" in form.errors


@pytest.mark.django_db
def test_authenticated_user_can_leave_review(client, user, published_ad):
    client.login(username="testuser", password="testpass123")

    url = reverse("reviews:add_review", kwargs={"pk": published_ad.pk})
    response = client.post(url, {"text": "Great ad!", "rating": 5})

    assert response.status_code == 302
    assert Review.objects.count() == 1

    review = Review.objects.get()
    assert review.ad == published_ad
    assert review.author == user
    assert review.text == "Great ad!"
    assert review.rating == 5


@pytest.mark.django_db
def test_anonymous_user_cannot_leave_review(client, published_ad):
    url = reverse("reviews:add_review", kwargs={"pk": published_ad.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_is_displayed_on_ad_detail(client, user, published_ad):
    Review.objects.create(
        ad=published_ad,
        text="Nice product",
        rating=4,
        author=user,
    )

    response = client.get(reverse("ads:ad_detail", kwargs={"pk": published_ad.pk}))
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Nice product" in content
    assert "4" in content
