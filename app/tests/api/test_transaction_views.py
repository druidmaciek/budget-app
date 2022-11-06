import pytest

from api.models import Transaction

@pytest.mark.django_db
def test_add_transaction(client, add_user, add_budget):
    user = add_user()
    budget = add_budget(name="my budget", description="ok budget", owner=user)
    client.force_login(user)

    transactions = Transaction.objects.all()
    assert len(transactions) == 0

    response = client.post(
        "/api/transactions/",
        {
            "name": "Rent",
            "category": "rent",
            "type": "expense",
            "amount": 200000,
            "budget": budget.id,
        },
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "Rent"
    assert response.data["amount"] == 200000
    assert response.data["type"] == "expense"
    assert response.data["budget"] == budget.id
    assert response.data["owner"] == user.id

    transactions = Transaction.objects.all()
    assert len(transactions) == 1


@pytest.mark.django_db
def test_get_all_transactions(client, add_budget, add_user, add_transaction):
    user = add_user()
    client.force_login(user)
    budget = add_budget(
        name="My Family Budget", description="our budget", owner=user
    )
    transaction_one = add_transaction(name="rent", type="expense", category="rent", budget=budget, amount=200000)
    transaction_two = add_transaction(name="salary", type="income", category="salary", budget=budget, amount=500000)
    
    response = client.get("/api/transactions/")
    assert response.status_code == 200
    assert response.data["results"][0]["name"] == transaction_one.name
    assert response.data["results"][1]["name"] == transaction_two.name