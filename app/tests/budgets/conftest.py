import pytest

from budgets.models import Budget


@pytest.fixture(scope="function")
def add_budget():
    def _add_budget(name, description):
        return Budget.objects.create(name=name, description=description)

    return _add_budget
