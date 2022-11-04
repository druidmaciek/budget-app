import pytest

from budgets.serializers import BudgetSerializer, UserSerializer


def test_valid_budget_serializer():
    valid_serializer_data = {
        "name": "My Family Budget",
        "description": "This is our budget",
    }
    serializer = BudgetSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_budget_serializer():
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
