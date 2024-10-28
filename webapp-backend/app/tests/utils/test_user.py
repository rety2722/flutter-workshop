from app import crud, schemas
from app.core.config import settings
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .utils import random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}{settings.TOKEN_ROUTE_PATH}", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.get_user_by_email(session=db, email=email)
    if not user:
        user_in_create = schemas.UserCreate(
            email=email, password=password, full_name="Test Eblan"
        )
        user = crud.create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = schemas.UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = crud.update_user(session=db, user=user, user_in=user_in_update)
    return user_authentication_headers(client=client, email=email, password=password)