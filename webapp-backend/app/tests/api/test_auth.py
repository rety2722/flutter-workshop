from fastapi.testclient import TestClient

from app.core.config import settings


def test_signup(client: TestClient) -> None:
    responce = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "john@auth.com",
            "password": "123456",
            "full_name": "John John",
        },
    )
    assert responce.status_code == 200


def test_signup_existing(client: TestClient) -> None:
    responce = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "john@auth.com",
            "password": "123456",
            "full_name": "John John",
        },
    )
    assert responce.status_code == 400


def test_signin(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/signin",
        data={
            "username": "john@auth.com",
            "password": "123456",
        },
    )
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_signin_incorrect(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/signin",
        data={"username": "incorrect@auth.com", "password": "eblanchik"},
    )
    assert r.status_code == 400