from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

from fastapi import APIRouter, Request, Response
from ano_captcha.generate import b64_captcha
from fastapi.responses import JSONResponse

captcharouter = APIRouter(
    prefix="/captcha",
    tags=["Captcha"]
)


@captcharouter.get("/getCaptcha")
async def get_captcha(
        request: Request,
        ttl: int = 1800
):
    while True:
        b64_img, code = b64_captcha()
        redis_has = await request.app.state.redis.get(code)
        if redis_has is None:
            break

    # 为了不区分大小写，将code中的字母全改为小写
    code_lower = ""
    for i in code:
        if i.isalpha():
            code_lower += i.lower()
        else:
            code_lower += i
    response = {
        "image": b64_img,
        "code": code_lower,
        "ttl": ttl
    }

    # 无状态cache验证
    await request.app.state.redis.set(name=code_lower, value=b64_img, ex=ttl)
    # return JSONResponse(status_code=200, content=response)

    # 有状态验证
    resp = JSONResponse(content=response)
    resp.set_cookie(key="captcha_session", value=code, expires=ttl)
    return resp


@captcharouter.get("/login")
async def user_login(request: Request, image: str, code: str):
    code_lower = ""
    for i in code:
        if i.isalpha():
            code_lower += i.lower()
        else:
            code_lower += i

    # 无状态cache验证
    try:
        v = await request.app.state.redis.get(code_lower)
    except Exception as e:
        return JSONResponse(status_code=500, content=e)
    redis_value: str = v.decode('utf-8')
    if redis_value != image:
        return JSONResponse(status_code=500, content=redis_value)
    return JSONResponse(status_code=200, content="login successful!")
