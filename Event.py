from fastapi import FastAPI
from typing import Callable

from database_redis import register_redis


def event_startup(app: FastAPI) -> Callable:
    async def app_start() -> None:
        await register_redis(app)

    return app_start


def event_shutdown(app: FastAPI) -> Callable:
    async def app_drop() -> None:
        pass

    return app_drop
