import os

import httpx

from app.config import Config, ProductionConfig

config = ProductionConfig if os.getenv("FLASK_ENV") == "production" else Config

def create_user(request):
    data = request.form
    if not data:
        return None, ("missing form data", 404)
    response = httpx.post(config.AUTH_USER_REGISTRATION, data=data, timeout=10.0)
    if response.status_code == 200:
        return
    else:
        return (response.text, response.status_code)


# get basic auth and post to auth login endpoint, return jwt token
def get_jwt(request):
    data = request.form
    if not data:
        return None, ("missing credentials", 401)
    basic = (data["username"], data["password"])
    response = httpx.post(config.AUTH_CREATE_JWT, auth=basic, timeout=10.0)
    if response.status_code == 200:
        return response.cookies, None
    else:
        return None, response.text


def validate_jwt(request):
    headers = {"X-CSRF-TOKEN": request.cookies.get("csrf_access_token")}
    response = httpx.post(
        config.AUTH_VALIDATE_JWT,
        cookies=request.cookies,
        headers=headers,
        timeout=10.0
    )
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def logout_user(request):
    headers = {"X-CSRF-TOKEN": request.cookies.get("csrf_access_token")}
    response = httpx.post(
        config.AUTH_LOGOUT,
        cookies=request.cookies,
        headers=headers,
        timeout=10.0
    )
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def add_auth_cookies(response, cookies):
    response.set_cookie(
        "access_token_cookie",
        cookies.get("access_token_cookie"),
        httponly=True,
        secure=True,
        samesite="none",
    )
    response.set_cookie(
        "refresh_token_cookie",
        cookies.get("refresh_token_cookie"),
        httponly=True,
        secure=True,
        samesite="none",
        path=config.JWT_REFRESH_PATH,
    )
    response.set_cookie(
        "csrf_access_token",
        cookies.get("csrf_access_token"),
        secure=True,
        samesite="none",
    )
    response.set_cookie(
        "csrf_refresh_token",
        cookies.get("csrf_refresh_token"),
        secure=True,
        samesite="none",
        path=config.JWT_REFRESH_PATH,
    )
    return response
