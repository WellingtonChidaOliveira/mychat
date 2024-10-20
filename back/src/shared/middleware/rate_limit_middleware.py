
import time
from typing import Dict
from ..infrastructure.redis import redis


class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        
    async def is_allowed(self, client_ip: str, limit: int, period: int) -> bool:
        """Rate limiter for WebSocket connections."""
        current_time = int(time.time())
        key = f"rate_limiter:{client_ip}:{current_time // period}"  
        
        # Increment the counter in Redis
        current_count = await redis.incr(key)
        
        if current_count == 1:
            await redis.expire(key, period)  # Set expiration for this time window

        if current_count > limit:
            return False  # Rate limit exceeded

        return True  # Rate limit OK