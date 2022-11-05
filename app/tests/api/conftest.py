import random
import string

import pytest
from django.contrib.auth import get_user_model

from api.models import Budget


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def create_user(username="email@example.com", password="passworD123!"):
    return get_user_model().objects.create_user(
        username=username, first_name="Test", last_name="User", password=password
    )


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username="email@example.com", password="passworD123!"):
        user = create_user(username, password)
        return user

    return _add_user


@pytest.fixture(scope="function")
def add_budget():
    def _add_budget(name, description, owner=None):
        if owner is None:
            owner = create_user()
        return Budget.objects.create(name=name, description=description, owner=owner)

    return _add_budget
