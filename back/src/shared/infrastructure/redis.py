# back/src/shared/infrastructure/redis_client.py
import redis.asyncio as aioredis
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)