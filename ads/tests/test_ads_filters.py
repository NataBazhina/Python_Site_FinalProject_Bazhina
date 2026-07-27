import pytest
from django.test import Client

from django.contrib.auth.models import User
from ads.models import Ad
from ads.views import ad_list


@pytest.mark.django_db
def test_search_finds_by_title():
    """Поиск находит объявление по слову из заголовка"""
    user = User.objects.create_user(username="testuser", password="testpass123")

    Ad.objects.create(
        title="Платье вечернее",
        description="Красивое вечернее платье для торжеств",
        location="Москва",
        price=5000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Джинсы мужские",
        description="Стильные мужские джинсы",
        location="Москва",
        price=2000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Платье летнее",
        description="Летнее платье из лёгкой ткани",
        location="СПб",
        price=3000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Костюм деловой",
        description="Деловой костюм для офиса",
        location="СПб",
        price=7000,
        status="published",
        author=user,
    )

    client = Client()
    response = client.get("/ads/", {"q": "платье"})

    # Получить ads из response
    ads = response.context["ads"]

    assert ads.count() == 2
    assert any(ad.title == "Платье вечернее" for ad in ads)
    assert any(ad.title == "Платье летнее" for ad in ads)


@pytest.mark.django_db
def test_search_finds_by_description():
    """Поиск находит объявление по слову из описания"""
    user = User.objects.create_user(username="testuser", password="testpass123")

    Ad.objects.create(
        title="Платье вечернее",
        description="Красивое вечернее платье для торжеств",
        location="Москва",
        price=5000,
        status="published",
        author=user,
    )

    client = Client()
    response = client.get("/ads/", {"q": "вечернее"})
    ads = response.context["ads"]

    assert ads.count() == 1
    assert ads.first().title == "Платье вечернее"


@pytest.mark.django_db
def test_filter_by_location():
    """Фильтр по месту возвращает только нужные объявления"""
    user = User.objects.create_user(username="testuser", password="testpass123")

    Ad.objects.create(
        title="Платье вечернее",
        description="Красивое вечернее платье для торжеств",
        location="Москва",
        price=5000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Платье летнее",
        description="Летнее платье из лёгкой ткани",
        location="СПб",
        price=3000,
        status="published",
        author=user,
    )

    client = Client()
    response = client.get("/ads/", {"location": "Москва"})
    ads = response.context["ads"]

    assert ads.count() == 1
    assert ads.first().location == "Москва"


@pytest.mark.django_db
def test_filter_by_price():
    """Фильтр по цене возвращает корректный набор"""
    user = User.objects.create_user(username="testuser", password="testpass123")

    Ad.objects.create(
        title="Платье вечернее",
        description="Красивое вечернее платье для торжеств",
        location="Москва",
        price=5000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Платье летнее",
        description="Летнее платье из лёгкой ткани",
        location="СПб",
        price=3000,
        status="published",
        author=user,
    )

    client = Client()
    response = client.get("/ads/", {"price_to": 4000})
    ads = response.context["ads"]

    assert ads.count() == 1
    assert ads.first().price == 3000


@pytest.mark.django_db
def test_combined_search_and_filters():
    """Комбинированный запрос работает правильно"""
    user = User.objects.create_user(username="testuser", password="testpass123")

    Ad.objects.create(
        title="Платье вечернее",
        description="Красивое вечернее платье для торжеств",
        location="Москва",
        price=5000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Платье летнее",
        description="Летнее платье из лёгкой ткани",
        location="СПб",
        price=3000,
        status="published",
        author=user,
    )
    Ad.objects.create(
        title="Костюм деловой",
        description="Деловой костюм для офиса",
        location="СПб",
        price=7000,
        status="published",
        author=user,
    )

    client = Client()
    response = client.get("/ads/", {
        "q": "платье",
        "location": "СПб",
        "price_from": 2000,
        "price_to": 4000,
    })
    ads = response.context["ads"]

    assert ads.count() == 1
    assert ads.first().title == "Платье летнее"
    assert ads.first().location == "СПб"
    assert ads.first().price == 3000
