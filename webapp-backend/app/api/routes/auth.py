from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post(
    "/signup", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED
)
def register_user(session: SessionDep, user_in: schemas.UserRegister) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server right now",
        )
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    user_create = schemas.UserCreate.model_validate(
        user_in.model_dump(exclude_unset=True)
    )
    user = crud.create_user(session=session, user_create=user_create)
    return user


@router.post("/signin", response_model=schemas.Token)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.Token:
    try:
        user = crud.authenticate(
            session=session, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
        access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    except Exception as e:
        raise e

    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
