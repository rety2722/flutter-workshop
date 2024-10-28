from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.core.db import SessionLocal
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.execute(delete(models.User))
        db.execute(delete(models.Event))
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
