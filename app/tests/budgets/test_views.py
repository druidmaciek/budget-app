import pytest

from budgets.models import Budget


@pytest.mark.django_db
def test_add_budget(client):
    budgets = Budget.objects.all()
    assert len(budgets) == 0

    response = client.post(
        "/api/budgets/",
        {
            "name": "My Family Budget",
            "description": "Our Budget",
        },
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "My Family Budget"

    budgets = Budget.objects.all()
    assert len(budgets) == 1


@pytest.mark.django_db
def test_add_budget_invalid_json(client):
    budgets = Budget.objects.all()
    assert len(budgets) == 0

    response = client.post(
        "/api/budgets/",
        {},
        content_type="application/json",
    )
    assert response.status_code == 400

    budgets = Budget.objects.all()
    assert len(budgets) == 0


@pytest.mark.django_db
def test_add_budget_invalid_json_keys(client):
    budgets = Budget.objects.all()
    assert len(budgets) == 0

    response = client.post(
        "/api/budgets/",
        {"description": "description"},
        content_type="application/json",
    )
    assert response.status_code == 400

    budgets = Budget.objects.all()
    assert len(budgets) == 0


@pytest.mark.django_db
def test_get_single_budget(client, add_budget):
    budget = add_budget(name="My Family Budget", description="my budget")
    response = client.get(f"/api/budgets/{budget.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "My Family Budget"


def test_get_single_budget_incorrect_id(client):
    response = client.get("/api/budgets/incorrect/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_budgets(client, add_budget):
    budget_one = add_budget(name="My Family Budget", description="our budget")
    budget_two = add_budget(name="My Personal Budget", description="my budget")
    response = client.get("/api/budgets/")
    assert response.status_code == 200
    assert response.data[0]["name"] == budget_one.name
    assert response.data[1]["name"] == budget_two.name
