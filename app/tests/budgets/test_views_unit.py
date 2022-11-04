import pytest
from django.http import Http404

from budgets.views import BudgetSerializer, BudgetViewSet, Budget


def test_add_budget(client, monkeypatch):
    payload = {"name": "Our Budget", "description": "This is our budget"}

    def mock_create(self, payload):
        return "Our Budget"

    monkeypatch.setattr(BudgetSerializer, "create", mock_create)
    monkeypatch.setattr(BudgetSerializer, "data", payload)

    resp = client.post("/api/budgets/", payload, content_type="application/json")
    assert resp.status_code == 201
    assert resp.data["name"] == "Our Budget"


def test_add_budget_invalid_json(client):
    resp = client.post("/api/budgets/", {}, content_type="application/json")
    assert resp.status_code == 400


def test_add_budget_invalid_json_keys(client):
    resp = client.post(
        "/api/budgets/",
        {"description": "our budget"},
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_get_single_budget(client, monkeypatch):
    payload = {"name": "Our Budget", "description": "This is our budget"}

    def mock_get_object(pk):
        return 1

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)
    monkeypatch.setattr(BudgetSerializer, "data", payload)

    resp = client.get("/api/budgets/1/")
    assert resp.status_code == 200
    assert resp.data["name"] == "Our Budget"


def test_get_single_budget_incorrect_id(client):
    resp = client.get("/api/budgets/incorrect/")
    assert resp.status_code == 404


def test_remove_budget(client, monkeypatch):
    def mock_get_object(self, pk):
        class Budget:
            def delete():
                pass

        return Budget

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)


def test_remove_budget_incorrect_id(client, monkeypatch):
    def mock_get_object(pk):
        raise Http404

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)

    resp = client.delete("/api/budgets/incorrect/")
    assert resp.status_code == 404


def test_update_budget(client, monkeypatch):
    payload = {"name": "Our Budget", "description": "This is our budget"}

    def mock_get_object(pk):
        return 1

    def mock_update_object(self, movie_object, data):
        return payload

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)
    monkeypatch.setattr(BudgetSerializer, "update", mock_update_object)

    resp = client.put("/api/budgets/1/", payload, content_type="application/json",)
    assert resp.status_code == 200
    assert resp.data["name"] == payload["name"]
    assert resp.data["description"] == payload["description"]

def test_update_budget_incorrect_id(client, monkeypatch):
    def mock_get_object(pk):
        raise Http404

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)

    resp = client.put("/api/budgets/incorrect/")
    assert resp.status_code == 404


@pytest.mark.parametrize(
    "payload, status_code",
    [[{}, 400], [{"description": "our budget"}, 400]],
)
def test_update_budget_invalid_json(client, monkeypatch, payload, status_code):
    def mock_get_object(pk):
        return 1

    monkeypatch.setattr(BudgetViewSet, "get_object", mock_get_object)

    resp = client.put("/api/budgets/1/", payload, content_type="application/json",)
    assert resp.status_code == status_code