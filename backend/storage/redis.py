from abc import ABC, abstractmethod
from datetime import timedelta

from redis.asyncio import Redis


class AbstractKeyStorage(ABC):

    @abstractmethod
    async def set_value():
        raise NotImplementedError


class RedisStorage(AbstractKeyStorage):
    redis_client: Redis = None

    async def set_value(self, key: int, value: str, expire: timedelta):
        await self.redis_client.set(key, value)
        await self.redis_client.expire(key, expire)
