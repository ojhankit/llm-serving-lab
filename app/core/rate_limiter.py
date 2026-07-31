import time
from fastapi import Request
from app.core.config import settings
from app.core.exceptions import RateLimitExceededError

class RateLimiter:
    def __init__(self, requests: int, window_seconds: int):
        self.requests = requests
        self.window_seconds = window_seconds
        
        # Redis connection setup if configured
        self.redis = None
        if settings.RATE_LIMIT_BACKEND == "redis":
            import redis.asyncio as aioredis
            self.redis = aioredis.from_url(settings.REDIS_URL)

        # In-memory store: client_id -> list of timestamps
        self.in_memory_store = {}

    async def __call__(self, request: Request):
        # 1. Identify Client
        client_id = request.headers.get("X-Client-ID") or request.client.host
        now = time.time()
        
        if self.redis:
            # 2. Redis-backed Sliding Window Log
            key = f"rate_limit:{request.url.path}:{client_id}"
            cutoff = now - self.window_seconds
            
            async with self.redis.pipeline(transaction=True) as pipe:
                pipe.zremrangebyscore(key, 0, cutoff)
                pipe.zcard(key)
                pipe.zadd(key, {str(now): now})
                pipe.expire(key, self.window_seconds)
                _, current_requests, _, _ = await pipe.execute()
                
            if current_requests > self.requests:
                # Retrieve the oldest request timestamp in the window to calculate retry_after
                oldest = await self.redis.zrange(key, 0, 0, withscores=True)
                retry_after = oldest[0][1] + self.window_seconds - now if oldest else self.window_seconds
                raise RateLimitExceededError(self.requests, self.window_seconds, retry_after)
        else:
            # 3. In-memory Sliding Window Log
            key = f"{request.url.path}:{client_id}"
            timestamps = self.in_memory_store.setdefault(key, [])
            
            # Remove old entries
            self.in_memory_store[key] = [t for t in timestamps if t > now - self.window_seconds]
            timestamps = self.in_memory_store[key]
            
            if len(timestamps) >= self.requests:
                retry_after = timestamps[0] + self.window_seconds - now
                raise RateLimitExceededError(self.requests, self.window_seconds, retry_after)
                
            timestamps.append(now)