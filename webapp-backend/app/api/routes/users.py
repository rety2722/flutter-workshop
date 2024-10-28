from typing import Any

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import (
    SessionDep,
)

from app.schemas import (
    UserPublic,
    UsersPublic
)

router = APIRouter()


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(user_id: int, session: SessionDep) -> Any:
    user = crud.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
