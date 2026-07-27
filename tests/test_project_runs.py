import pytest
from django.core.management import call_command


def test_django_project_runs():
    """Тест запуска Django-проекта через call_command('check')"""
    call_command("check", fail_level="WARNING")
