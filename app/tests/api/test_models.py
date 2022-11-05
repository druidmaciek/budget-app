import pytest

from api.models import Transaction


@pytest.mark.django_db
def test_budget_model(add_user, add_budget):
    user = add_user()
    budget = add_budget(
        name="My Family Budget", description="This is our family budget", owner=user
    )
    assert budget.name == "My Family Budget"
    assert budget.description == "This is our family budget"
    assert budget.created_at
    assert budget.updated_at
    assert budget.owner == user
    assert str(budget) == budget.name


@pytest.mark.django_db
def test_transaction_model(add_budget):
    budget = add_budget(name="My Family Budget", description="Our Budget")
    transaction = Transaction(
        name="Rent for Apartment",
        amount=200000,
        category="rent",
        budget=budget,
        type="expense",
    )
    assert transaction.name == "Rent for Apartment"
    assert transaction.amount == 200000
    assert transaction.category == "rent"
    assert transaction.budget == budget
    assert transaction.type == "expense"
    assert str(transaction) == "Rent for Apartment (-2000.00)"
