from backend.storage.repository import SQLAlchemyRepository

from .model import Paste


class PastesRepository(SQLAlchemyRepository):
    model = Paste
