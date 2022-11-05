import pytest

from api.models import Budget


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
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"description": "description"},
    ],
)
def test_add_budget_invalid_json(client, payload):
    budgets = Budget.objects.all()
    assert len(budgets) == 0

    response = client.post(
        "/api/budgets/",
        payload,
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


@pytest.mark.django_db
def test_remove_budget(client, add_budget):
    budget = add_budget(name="My Family Budget", description="our budget")

    response = client.get(f"/api/budgets/{budget.id}/")
    assert response.status_code == 200
    assert response.data["name"] == budget.name

    response_two = client.delete(f"/api/budgets/{budget.id}/")
    assert response_two.status_code == 204

    response_three = client.get("/api/budgets/")
    assert response_three.status_code == 200
    assert len(response_three.data) == 0


@pytest.mark.django_db
def test_remove_budget_incorrect_id(client):
    response = client.delete("/api/budgets/incorrect/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_budget(client, add_budget):
    budget = add_budget(name="My Family Budget", description="our budget")

    response = client.put(
        f"/api/budgets/{budget.id}/",
        {"name": "Our Family Budget", "description": "our budget"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data["name"] == "Our Family Budget"
    assert response.data["description"] == "our budget"

    response_two = client.get(f"/api/budgets/{budget.id}/")
    assert response_two.status_code == 200
    assert response_two.data["name"] == "Our Family Budget"
    assert response_two.data["description"] == "our budget"


@pytest.mark.django_db
def test_update_budget_incorrect_id(client):
    response = client.put("/api/budgets/incorrect/")
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_budget, payload, status_code",
    [
        ["add_budget", {}, 400],
        ["add_budget", {"description": "the budget"}, 400],
    ],
    indirect=["add_budget"],
)
def test_update_budget_invalid_json(client, add_budget, payload, status_code):
    budget = add_budget(name="My Family Budget", description="our budget")
    response = client.put(
        f"/api/budgets/{budget.id}/", payload, content_type="application/json"
    )
    assert response.status_code == status_code
