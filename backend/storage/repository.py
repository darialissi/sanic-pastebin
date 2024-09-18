from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, session: AsyncSession, data: dict, **ids: int):
        stmt = insert(self.model).values(**data, **ids).returning(self.model)

        result = await session.execute(stmt)
        return result.scalar_one()

    async def get_one(self, session: AsyncSession, **filters):
        stmt = select(self.model)
        while filters:
            key, val = filters.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession, **filters):
        stmt = select(self.model)
        while filters:
            key, val = filters.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)

        result = await session.execute(stmt)
        return result.scalars().all()
