import pytest
from django.apps import apps

@pytest.mark.django_db
def test_apps_are_installed():
    """Проверка, что все приложения установлены"""
    assert apps.is_installed('ads')
    assert apps.is_installed('users')
    assert apps.is_installed('reviews')
    assert apps.is_installed('moderation')