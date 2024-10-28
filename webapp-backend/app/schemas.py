from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, model_validator


# user
class UserBase(BaseModel):
    full_name: str


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None


class User(UserBase):
    id: int
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True

    def __eq__(self, other):
        return self.id == other.id


# update
class UserUpdate(UserBase):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    hashed_password: str | None = None

    @model_validator(mode="after")
    def not_set_both(self):
        if self.password is not None and self.hashed_password is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="can't provide both password and hashed_password",
            )
        return self

    class Config:
        from_attirbutes = True


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


# public
class UserPublic(UserBase):
    id: int

    class Config:
        from_attributes = True

    def __eq__(self, other):
        return self.id == other.id


class UsersPublic(BaseModel):
    data: list["UserPublic"]
    count: int


# message
class Message(BaseModel):
    message: str


# token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None
