import redis.asyncio as redis

from .config import settings

REDIS_URL = str(settings.REDIS_URL)

pool = redis.ConnectionPool.from_url(REDIS_URL)
redis_client = redis.Redis(connection_pool=pool)
