from datetime import datetime
from typing import Set

from pydantic import BaseModel, ConfigDict, Field


class UserSchemaAdd(BaseModel):
    """
    Схема модели User, используется при создании
    """

    username: str = Field(min_length=5, max_length=30, pattern="^[A-Za-z0-9-_]+$")
    password: str = Field(min_length=5)


class UserSchema(BaseModel):
    """
    Общая схема модели User, валидирует ответы
    """

    id: int = Field(gt=0)
    username: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    pastes: Set

    model_config = ConfigDict(from_attributes=True)
