from base64 import b64encode

from sqlalchemy import select

from app.jwt_utils import create_access_JWT
from app.models import User


def test_create_user(client, session):
    '''
    test user creation via endpoint
    
    '''
    res = client.post(
        "/users/create", data=dict(username="test", password="test", email="test@t.com")
    )
    assert res.status_code == 200


def test_create_jw(client, session):
    '''
    test jwt creation on login via endpoint
    
    '''
    credentials = b64encode(b"test1:test1").decode("utf-8")
    res = client.post("/auth/login", headers={"Authorization": f"Basic {credentials}"})
    assert res.status_code == 200
    assert {"msg": "login successful"} in res.json
    assert "Set-Cookie" in res.headers


def test_fail_user_logged_in(client):
    '''
    test login failure
    
    '''
    with client:
        res = client.post("/auth/login", data=dict(username="test", password="test"))
        assert res.status_code == 401


def test_validate_jwt(client, user, session):
    '''
    test jwt validation via endpoint
    
    '''
    client.set_cookie("access_token_cookie", create_access_JWT(user.username, True))
    res = client.post("/auth/validate")
    assert user.username in res.json.values()


def test_logout_user(client, user, session):
    '''
    test logout via endpoint
    
    '''
    client.set_cookie("access_token_cookie", create_access_JWT(user.username, True))
    res = client.post("/auth/logout")
    assert res.status_code == 200
    assert {"msg": "logout successful"} in res.json


def test_users_list(client, user, session):
    '''
    test getting list of all users via endpoint
    
    '''
    client.set_cookie("access_token_cookie", create_access_JWT(user.username, True))
    res = client.get("/users/all")
    assert res.status_code == 200


def test_user_details(client, user, session):
    '''
    test getting user details from jwt claims via endpoint 
    
    '''
    client.set_cookie("access_token_cookie", create_access_JWT(user.username, True))
    res = client.get("/users/whoami")
    assert user.username in res.text