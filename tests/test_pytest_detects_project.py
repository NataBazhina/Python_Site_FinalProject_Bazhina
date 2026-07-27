import pytest
from django.conf import settings


def test_pytest_detects_django_project():
    """Проверка, что pytest видит проект и поднимает настройки"""
    assert settings.DATABASES
    assert settings.ROOT_URLCONF
    assert settings.WSGI_APPLICATION
