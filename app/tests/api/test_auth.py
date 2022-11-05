import base64
import json

import pytest
from django.contrib.auth import get_user_model

PASSWORD = "passworD123!"


@pytest.mark.django_db
def test_user_can_sign_up(client):
    response = client.post(
        "/api/register/",
        {
            "username": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": PASSWORD,
            "password2": PASSWORD,
        },
        content_type="application/json",
    )
    user = get_user_model().objects.last()
    assert response.status_code == 201
    assert response.data["id"] == user.id
    assert response.data["username"] == user.username
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name


@pytest.mark.django_db
def test_user_can_log_in(client, add_user):
    user = add_user()
    response = client.post(
        "/api/login/",
        {
            "username": user.username,
            "password": PASSWORD,
        },
    )
    assert response.status_code == 200

    access = response.data["access"]
    payload = access.split(".")[1]
    decoded_payload = base64.b64decode(f"{payload}==")
    payload_data = json.loads(decoded_payload)
    assert response.data.get("refresh") is not None
    assert payload_data["id"] == user.id
    assert payload_data["username"] == user.username
    assert payload_data["first_name"] == user.first_name
    assert payload_data["last_name"] == user.last_name
