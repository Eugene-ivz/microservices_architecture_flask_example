import datetime

from flask_jwt_extended import create_access_token, create_refresh_token
#from auth.views import jwt

def create_access_JWT(username, allowed=False, fresh=False):
    claims = {'allowed': allowed}
    return create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=20),
                               additional_claims=claims, fresh=fresh)
    
def create_refresh_JWT(username):
    return create_refresh_token(identity=username, expires_delta=datetime.timedelta(days=10))