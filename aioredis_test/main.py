import asyncio

import aioredis
import uvicorn
from aioredis import Redis
from fastapi import FastAPI
from typing import Callable
from pydantic import BaseModel

app = FastAPI()


async def register_redis(app: FastAPI):
    # redis://[[username]:[password]]@localhost:6379/0
    redis = aioredis.from_url("redis://default:li12345678@192.168.17.131:6379/2")
    app.state.redis = redis
    # await redis.set(name="key_name", value="value2222", ex=30)
    # value = await redis.get("key_name")
    # print(value)


# class AppState:
#     def __init__(self, some_data):
#         self.some_data = some_data


# 在应用程序启动时创建并配置state对象


def startup_event(app) -> Callable:
    async def app_start() -> None:
        # app.state = AppState(some_data="Hello, World!")
        # app.state.redis = await register_redis()
        await register_redis(app)

    return app_start


@app.post("/postredis")
async def post_redis(
        key_name: str = "captcha_code",
        value: str = "code_value",
        extime: int = 60,
):
    await app.state.redis.set(name=key_name, value=value, ex=extime)
    k = await app.state.redis.get("captcha_code")
    d = {
        "key_name": key_name,
        "value": value,
        "extime": extime,
        "k": k,
    }
    return d


if __name__ == "__main__":
    app.add_event_handler("startup", startup_event(app))
    uvicorn.run(app, port=8985)
