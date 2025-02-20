import pytest
from django.test import override_settings

@pytest.fixture(scope='session', autouse=True)
def django_db_setup():
    """Настройка базы данных для тестов."""
    with override_settings(DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }):
        yield