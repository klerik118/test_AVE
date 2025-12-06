from redis.asyncio import Redis


async def get_redis():
    redis_app = await Redis.from_url('redis://redis:6379', decode_responses=True)
    try:
        yield redis_app
    finally:
        await redis_app.close()