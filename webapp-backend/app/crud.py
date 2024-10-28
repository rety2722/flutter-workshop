from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from . import models, schemas


def create_user(*, session: Session, user_create: schemas.UserCreate) -> schemas.User:
    try:
        user_data = user_create.model_dump(exclude="password")
        user_data["hashed_password"] = get_password_hash(user_create.password)
        db_user = models.User(**user_data)
        session.add(db_user)
        session.commit()
    except Exception as e:
        raise e

    return schemas.User.model_validate(db_user)


def delete_user(*, session: Session, user: schemas.User) -> None:
    try:
        session.query(models.User).filter(models.User.id == user.id).delete()
        session.commit()
    except Exception as e:
        raise e


def update_user(
    *, session: Session, user: schemas.User, user_in: schemas.UserUpdate
) -> schemas.User | None:
    try:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            hashed_password = get_password_hash(user_data["password"])
            extra_data["hashed_password"] = hashed_password
            user_data.pop("password")

        update_data = user_data | extra_data

        session.query(models.User).filter(models.User.id == user.id).update(update_data)
        session.commit()
    except Exception as e:
        raise e

    user.__dict__.update(update_data)
    return user


def get_user_by_email(*, session: Session, email: str) -> schemas.User | None:
    try:
        db_user = session.query(models.User).filter(models.User.email == email).first()
    except Exception as e:
        raise e
    return schemas.User.model_validate(db_user) if db_user else None


def get_user_by_id(*, session: Session, user_id: int) -> schemas.User | None:
    try:
        db_user = session.query(models.User).filter(models.User.id == user_id).first()
    except Exception as e:
        raise e
    return schemas.User.model_validate(db_user) if db_user else None


def authenticate(*, session: Session, email: str, password: str) -> schemas.User | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
