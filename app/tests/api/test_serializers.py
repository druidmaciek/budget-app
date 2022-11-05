import pytest

from api.serializers import BudgetSerializer, TransactionSerializer, UserSerializer


@pytest.mark.django_db
def test_valid_transaction_serializer(add_budget):
    budget = add_budget(name="My Budget", description="my budget")
    valid_serializer_data = {
        "name": "Rent",
        "amount": 250000,
        "category": "rent",
        "budget": budget.id,
        "type": "expense",
    }
    serializer = TransactionSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == valid_serializer_data["name"]
    assert serializer.validated_data["amount"] == valid_serializer_data["amount"]
    assert serializer.validated_data["category"] == valid_serializer_data["category"]
    assert serializer.validated_data["budget"].id == valid_serializer_data["budget"]
    assert serializer.validated_data["type"] == valid_serializer_data["type"]
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_transaction_serializer(add_budget):
    budget = add_budget(name="My Budget", description="my budget")
    invalid_serializer_data = {
        "name": "Rent",
        "category": "rent",
        "budget": budget.id,
        "type": "expense",
    }
    serializer = TransactionSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"amount": ["This field is required."]}


@pytest.mark.django_db
def test_valid_budget_serializer(add_user):
    valid_serializer_data = {
        "name": "My Family Budget",
        "description": "This is our budget",
        "members": [],
    }
    serializer = BudgetSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data["members"] == []
    assert serializer.validated_data["name"] == "My Family Budget"
    assert serializer.validated_data["description"] == "This is our budget"
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_budget_serializer(add_user):
    invalid_serializer_data = {
        "description": "This is our budget",
    }
    serializer = BudgetSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_valid_user_serializer():
    valid_serializer_data = {
        "username": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password1": "CorrectPass123$",
        "password2": "CorrectPass123$",
    }
    serializer = UserSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data["username"] == "user@example.com"
    assert serializer.validated_data["first_name"] == "Test"
    assert serializer.validated_data["last_name"] == "User"
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_user_serializer():
    invalid_serializer_data = {
        "first_name": "Test",
        "last_name": "User",
        "password1": "CorrectPass123$",
        "password2": "CorrectPass123$",
    }
    serializer = UserSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"username": ["This field is required."]}


@pytest.mark.django_db
def test_password_not_matching_user_serializer():
    invalid_serializer_data = {
        "username": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password1": "CorrectPass123$",
        "password2": "CorrectPass134!",
    }
    serializer = UserSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"non_field_errors": ["Passwords must match."]}
