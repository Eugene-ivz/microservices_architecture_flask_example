from functools import wraps
import os
from joserfc import jwt
from joserfc.jwk import OctKey
from flask import jsonify, request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        else:
            return jsonify({'message' : 'Token is missing'}), 401
  
        try:
            data = jwt.decode(token, OctKey.import_key(os.getenv('JWT_SECRET')), algorithms=["HS256"])
            #TODO user model
            current_user = User.query\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f(current_user, *args, **kwargs)
    return decorated

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view