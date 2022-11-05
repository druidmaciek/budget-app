import pytest

from api.models import Budget


@pytest.mark.django_db
def test_budget_model():
    budget = Budget(name="My Family Budget", description="This is our family budget")
    budget.save()
    assert budget.name == "My Family Budget"
    assert budget.description == "This is our family budget"
    assert budget.created_at
    assert budget.updated_at
    assert str(budget) == budget.name
