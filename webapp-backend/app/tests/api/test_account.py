from fastapi.testclient import TestClient

from ..utils.utils import random_lower_string, random_email
from app.core.config import settings


def test_read_me(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/account", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user


def test_update_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    new_name = f"{random_lower_string()} {random_lower_string()}"
    r = client.patch(
        f"{settings.API_V1_STR}/account/update",
        headers=normal_user_token_headers,
        json={
            "full_name": new_name,
            "email": random_email(),
        },
    )
    assert r.status_code == 200
    response = r.json()
    assert "full_name" in response
    assert response["full_name"]