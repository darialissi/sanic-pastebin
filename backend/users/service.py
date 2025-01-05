from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.storage.repository import AbstractRepository
from backend.utils.auth.password import Password
from backend.utils.auth.token import Token
from config import settings

from .schema import UserSchema, UserSchemaAdd


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, session: AsyncSession, user: UserSchemaAdd):
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": Password.hash_password(password).decode("utf-8")})
        user = await self.users_repo.add_one(session, u_dict)
        await session.commit()
        return user

    def auth_user(self, user: UserSchema):
        payload = {"sub": str(user.id)}
        token = Token.encode_jwt(
            payload, private_key=settings.TOKEN_KEY_SECRET, expire=timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        )
        return token

    def get_auth_user_id(self, token: str):
        try:
            decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=token)
            return int(decoded.get("sub"))
        except:
            raise

    async def get_user(self, session: AsyncSession, **filters) -> UserSchema:
        user = await self.users_repo.get_one(session, **filters)
        return user
