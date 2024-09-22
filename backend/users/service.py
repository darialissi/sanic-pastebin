from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.storage.repository import AbstractRepository
from backend.utils.auth.password import Password
from backend.utils.auth.token import Token
from config import settings

from .schema import UserSchema


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, session: AsyncSession, user: dict):
        password = user.pop("password")
        user.update({"hashed_password": Password.hash_password(password).decode("utf-8")})
        user = await self.users_repo.add_one(session, user)
        await session.commit()
        return user

    async def auth_user(self, user: UserSchema):
        payload = {"sub": user.id}
        token = Token.encode_jwt(
            payload, private_key=settings.TOKEN_KEY_SECRET, expire=timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        )
        return token

    async def get_user(self, session: AsyncSession, **filters) -> UserSchema:
        user = await self.users_repo.get_one(session, **filters)
        return user
