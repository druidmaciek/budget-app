from budgets.serializers import BudgetSerializer


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
