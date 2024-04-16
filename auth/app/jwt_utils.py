import datetime

from flask_jwt_extended import create_access_token, create_refresh_token


def create_access_JWT(username, allowed=False, fresh=False):
    '''
    create access jwt token with username and allowed roles
    
    :param username: username of user
    :param allowed: allowed roles
    :param fresh: fresh token
    :return: access jwt token
    
    '''
    claims = {"allowed": allowed}
    return create_access_token(
        identity=username,
        expires_delta=datetime.timedelta(minutes=20),
        additional_claims=claims,
        fresh=fresh,
    )


def create_refresh_JWT(username):
    '''
    create refresh jwt token with username
    
    :param username: username of user
    :return: refresh jwt token
    
    '''
    return create_refresh_token(
        identity=username, expires_delta=datetime.timedelta(days=10)
    )
