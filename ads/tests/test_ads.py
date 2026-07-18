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
    assert ad.status == Ad.Status.PUBLISHED


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


@pytest.mark.django_db
def test_ad_detail_page_shows_data(client, user):
    ad = Ad.objects.create(
        title="Detail ad",
        description="Detail description",
        price="200.00",
        location="Moscow",
        contact="detail@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    url = reverse("ads:detail", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Detail ad" in content
    assert "Detail description" in content
    assert "Moscow" in content


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

#тесты для проверки архивации
@pytest.mark.django_db
def test_anonymous_cannot_archive_ad(client, ad):
    url = reverse("ads:archive", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("users:login") in response.url
    assert f"next={url}" in response.url


@pytest.mark.django_db
def test_user_cannot_archive_other_users_ad(client, other_user, ad):
    client.login(username="otheruser", password="testpass456")

    url = reverse("ads:archive", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_author_can_archive_own_ad(client, user, ad):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:archive", kwargs={"pk": ad.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("ads:my_ads")

    ad_updated = Ad.objects.get(pk=ad.pk)
    assert ad_updated.status == Ad.Status.ARCHIVED


@pytest.mark.django_db
def test_archived_ad_is_not_on_home_page(client, user, ad):
    client.login(username="testuser", password="testpass123")

    # Сначала архивируем объявление
    url = reverse("ads:archive", kwargs={"pk": ad.pk})
    client.get(url)

    # Создаем опубликованное объявление
    published_ad = Ad.objects.create(
        title="Published ad",
        description="Published description",
        price="200.00",
        location="Moscow",
        contact="published@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    url = reverse("ads:home")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Published ad" in content
    assert "Test ad" not in content


@pytest.mark.django_db
def test_archified_ad_appears_in_my_ads_with_archived_status(client, user, ad):
    client.login(username="testuser", password="testpass123")

    # Архивируем объявление
    url = reverse("ads:archive", kwargs={"pk": ad.pk})
    client.get(url)

    url = reverse("ads:my_ads")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Test ad" in content
    assert "archived" in content


@pytest.mark.django_db
def test_author_cannot_archive_already_archived_ad(client, user, ad):
    client.login(username="testuser", password="testpass123")

    url = reverse("ads:archive", kwargs={"pk": ad.pk})

    # первый раз
    response1 = client.get(url)
    assert response1.status_code == 302

    # второй раз
    response2 = client.get(url)
    assert response2.status_code == 302
    assert response2.url == reverse("ads:my_ads")

    ad_updated = Ad.objects.get(pk=ad.pk)
    assert ad_updated.status == Ad.Status.ARCHIVED

@pytest.mark.django_db
def test_my_ads_shows_all_statuses(client, user):
    client.login(username="testuser", password="testpass123")

    # Создаем объявления с разными статусами
    draft_ad = Ad.objects.create(
        title="Draft ad",
        description="Draft description",
        price="100.00",
        location="Moscow",
        contact="draft@example.com",
        author=user,
        status=Ad.Status.DRAFT,
    )

    published_ad = Ad.objects.create(
        title="Published ad",
        description="Published description",
        price="200.00",
        location="Moscow",
        contact="published@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    archived_ad = Ad.objects.create(
        title="Archived ad",
        description="Archived description",
        price="300.00",
        location="Moscow",
        contact="archived@example.com",
        author=user,
        status=Ad.Status.ARCHIVED,
    )

    url = reverse("ads:my_ads")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Draft ad" in content
    assert "draft" in content
    assert "Published ad" in content
    assert "published" in content
    assert "Archived ad" in content
    assert "archived" in content


@pytest.mark.django_db
def test_my_ads_filter_by_status_archived(client, user):
    client.login(username="testuser", password="testpass123")

    # Создаем объявления с разными статусами
    Ad.objects.create(
        title="Draft ad",
        description="Draft description",
        price="100.00",
        location="Moscow",
        contact="draft@example.com",
        author=user,
        status=Ad.Status.DRAFT,
    )

    Ad.objects.create(
        title="Published ad",
        description="Published description",
        price="200.00",
        location="Moscow",
        contact="published@example.com",
        author=user,
        status=Ad.Status.PUBLISHED,
    )

    Ad.objects.create(
        title="Archived ad",
        description="Archived description",
        price="300.00",
        location="Moscow",
        contact="archived@example.com",
        author=user,
        status=Ad.Status.ARCHIVED,
    )

    url = reverse("ads:my_ads") + "?status=archived"
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode(response.charset)
    assert "Archived ad" in content
    assert "Draft ad" not in content
    assert "Published ad" not in content