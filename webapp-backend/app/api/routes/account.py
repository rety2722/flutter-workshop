from typing import Any

from fastapi import APIRouter, HTTPException, status

from app import crud, schemas
from app.api.deps import CurrentUser, SessionDep
from app.core import security

router = APIRouter()


@router.get("/", response_model=schemas.UserPublic)
def read_user_me(*, current_user: CurrentUser) -> Any:
    return current_user


@router.patch("/update", response_model=schemas.UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: schemas.UserUpdate, current_user: CurrentUser
) -> Any:
    if user_in.password is not None or user_in.hashed_password is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update password data in this request. Try using update_password_me",
        )
    if user_in.email is not None:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    crud.update_user(session=session, user=current_user, user_in=user_in)
    return current_user


@router.patch(
    "/update-password",
    response_model=schemas.Message,
)
def update_password_me(
    *, session: SessionDep, body: schemas.UpdatePassword, current_user: CurrentUser
) -> Any:
    if not security.verify_password(
        body.current_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current one",
        )
    hashed_password = security.get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password

    crud.update_user(
        session=session,
        user=current_user,
        user_in=schemas.UserUpdate(hashed_password=hashed_password),
    )

    return schemas.Message(message="updated successfully")


@router.delete("/delete", response_model=schemas.Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    crud.delete_user(session=session, user=current_user)
    return schemas.Message(message=status.HTTP_204_NO_CONTENT + "")
