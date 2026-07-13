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
        status=Ad.Status.DRAFT,
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
def test_anonymous_does_not_see_contact(client, user):
    ad = Ad.objects.create(
        title="Detail ad",
        description="Detail description",
        price="200.00",
        location="Moscow",
        contact="detail@example.com",
        author=user,
        status=Ad.Status.DRAFT,
    )

    url = reverse("ads:detail", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "detail@example.com" not in content
    assert "Контакт доступен только авторизованным пользователям" in content


@pytest.mark.django_db
def test_user_cannot_edit_other_users_ad(client, other_user, ad):
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


@pytest.mark.django_db
def test_failed_ad_creation_with_empty_fields(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "",
        "description": "",
        "price": "150.00",
        "location": "Moscow",
        "contact": "test@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert "title" in response.context["form"].errors or "description" in response.context["form"].errors


@pytest.mark.django_db
def test_successful_ad_creation(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "Auto author ad",
        "description": "Test description",
        "price": "100.00",
        "location": "Saint Petersburg",
        "contact": "owner@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("home")
    ad = Ad.objects.get(title="Auto author ad")
    assert ad.author == user
    assert ad.status == Ad.Status.DRAFT


@pytest.mark.django_db
def test_author_is_set_automatically(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "Auto author ad 2",
        "description": "Test description",
        "price": "120.00",
        "location": "Moscow",
        "contact": "owner@example.com",
    }

    client.post(url, data)

    ad = Ad.objects.get(title="Auto author ad 2")
    assert ad.author == user


@pytest.mark.django_db
def test_ad_has_default_status(client, user):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:create")
    data = {
        "title": "Draft ad",
        "description": "Test",
        "price": "50.00",
        "location": "Moscow",
        "contact": "test@example.com",
    }

    client.post(url, data)

    ad = Ad.objects.get(title="Draft ad")
    assert ad.status == Ad.Status.DRAFT


@pytest.mark.django_db
def test_ad_detail_page_shows_data(client, user):
    ad = Ad.objects.create(
        title="Detail ad",
        description="Detail description",
        price="200.00",
        location="Moscow",
        contact="detail@example.com",
        author=user,
        status=Ad.Status.DRAFT,
    )

    url = reverse("ads:detail", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Detail ad" in content
    assert "Detail description" in content
    assert "Moscow" in content
    assert "draft" in content


@pytest.mark.django_db
def test_authenticated_user_sees_contact(client, user):
    client.login(username="testuser", password="testpass123")

    ad = Ad.objects.create(
        title="Detail ad",
        description="Detail description",
        price="200.00",
        location="Moscow",
        contact="detail@example.com",
        author=user,
        status=Ad.Status.DRAFT,
    )

    url = reverse("ads:detail", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "detail@example.com" in content
