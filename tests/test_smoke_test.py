import pytest
from django.core.management import call_command


def test_smoke_test_django_check():
    """Базовый smoke-тест — аналог python manage.py check"""
    try:
        call_command("check", fail_level="WARNING")
    except Exception as e:
        pytest.fail(f"Django check failed: {e}")
