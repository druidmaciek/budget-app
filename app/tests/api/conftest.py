import pytest
from django.contrib.auth import get_user_model

from api.models import Budget


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username="user@example.com", password="passworD123!"):
        return get_user_model().objects.create_user(
            username=username, first_name="Test", last_name="User", password=password
        )

    return _add_user


@pytest.fixture(scope="function")
def add_budget():
    def _add_budget(name, description):
        return Budget.objects.create(name=name, description=description)

    return _add_budget
