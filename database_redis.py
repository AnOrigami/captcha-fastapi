import aioredis
from fastapi import FastAPI


async def register_redis(app: FastAPI):
    # redis://[[username]:[password]]@localhost:6379/0
    redis = aioredis.from_url("redis://default:li12345678@192.168.17.131:6379/2")
    app.state.redis = redis
    # await redis.set(name="key_name", value="value2222", ex=30)
    # value = await redis.get("key_name")
    # print(value)
