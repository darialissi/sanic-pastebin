from redis.asyncio import Redis

from backend.storage.redis import RedisStorage
from config import settings


class TokenStorage(RedisStorage):
    redis_client = Redis.from_url(settings.REDIS_URL)
