from __future__ import annotations
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    text,
)
from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    hashed_password = Column(String, nullable=False)

    time_registered = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


    def __eq__(self, other: User):
        return self.id == other.id


