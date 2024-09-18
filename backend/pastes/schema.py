from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PasteURI(BaseModel):
    """
    Схема PasteURI, описывает формат
    """

    uri: str = Field(pattern=r"^[a-f\d]{8}$")


class PasteSchemaAdd(BaseModel):
    """
    Схема модели Paste, используется при создании
    """

    text: str  # --> s3


class PasteSchema(PasteURI, PasteSchemaAdd):
    """
    Общая схема модели Paste, валидирует ответы
    """

    id: int
    created_at: datetime
    expired_at: datetime

    user_id: int

    model_config = ConfigDict(from_attributes=True)
