import os
from flask import g, jsonify, redirect, url_for, Response
import httpx

def create_user(request):
    data = request.form
    if not data:
        return None, ("missing form data", 404)
    response = httpx.post(f'http://{os.getenv("FLASK_AUTH_USER_REGISTRATION")}', data=data)
    if response.status_code == 200:
        return
    else:
        return (response.text, response.status_code)

#get basic auth and post to auth login endpoint, return jwt token
def get_jwt(request):
    data = request.form
    if not data:
        return None, ("missing credentials", 401)
    basic = (data['username'], data['password'])
    response = httpx.post(
        f'http://{os.getenv("FLASK_AUTH_CREATE_JWT")}', auth=basic)
    if response.status_code == 200:
        return response.cookies, None
    else:
        return None, response.text
    
def validate_jwt(request):
    response = httpx.post(f'http://{os.getenv("FLASK_AUTH_VALIDATE_JWT")}')
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def logout_user(request):
    headers = {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    response = httpx.post(f'http://{os.getenv("FLASK_AUTH_LOGOUT")}',
                          cookies=request.cookies, headers=headers)
    if response.status_code == 200:
        print(response.text)
        return response.text, None
    else:
        print(response.text)
        return None, (response.text, response.status_code)
