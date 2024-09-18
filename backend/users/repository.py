from backend.storage.repository import SQLAlchemyRepository

from .model import User


class UsersRepository(SQLAlchemyRepository):
    model = User
