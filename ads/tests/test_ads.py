import pytest
from django.urls import reverse

from ads.models import Ad


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
        password="testpass456",
    )


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        title="Test ad",
        description="Test description",
        price="100.00",
        location="Moscow",
        contact="test@example.com",
        author=user,
    )


@pytest.mark.django_db
def test_anonymous_cannot_create_ad(client):
    url = reverse("ads:create")
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("users:login") in response.url
    assert f"next={url}" in response.url


@pytest.mark.django_db
def test_authenticated_user_can_create_ad(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "New ad",
        "description": "New description",
        "price": "250.00",
        "location": "Saint Petersburg",
        "contact": "owner@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("home")
    assert Ad.objects.filter(title="New ad", author=user).exists()


@pytest.mark.django_db
def test_anonymous_does_not_see_contact(client, ad):
    url = reverse("ads:detail", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "test@example.com" not in content
    assert "Контакт доступен только авторизованным пользователям" in content


@pytest.mark.django_db
def test_user_cannot_edit_other_users_ad(client, user, other_user, ad):
    client.login(username="otheruser", password="testpass456")

    url = reverse("ads:edit", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_anonymous_redirected_to_login_on_edit(client, ad):
    url = reverse("ads:edit", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("users:login") in response.url
    assert f"next={url}" in response.url
