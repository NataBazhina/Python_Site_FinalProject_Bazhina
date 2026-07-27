import pytest
from django.db import connection


@pytest.mark.django_db
def test_database_connection_in_test_env():
    """Тест подключения к БД в тестовой среде"""
    connection.ensure_connection()
    assert connection.is_usable()
