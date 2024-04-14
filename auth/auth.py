from flask import Blueprint, flash, jsonify, make_response, request, url_for
from flask_jwt_extended import (current_user, get_jwt, get_jwt_identity,
                                jwt_required, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from sqlalchemy import select

from auth.extensions import db
from auth.hashing import verify_password
from auth.jwt_utils import create_access_JWT, create_refresh_JWT
from auth.models import TokenBlocklist, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def create_jwt():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    try:
        user = db.session.scalar(select(User).where(User.username == auth.username))
        if not verify_password(auth.password, user.password) or not user.is_active:
            return "invalid credentials", 401
        else:
            user.is_authenticated = True
            db.session.add(user)
            db.session.commit()
            try:
                access_token = create_access_JWT(auth.username, True, True)
                refresh_token = create_refresh_JWT(auth.username)
            except Exception as e:
                return "invalid credentials 1", 401
            response = jsonify({"msg": "login successful"}, 200)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
    except Exception as e:
        return "invalid credentials 2", 401


@auth_bp.route("/validate", methods=["POST"])
@jwt_required()
def validate_jwt():
    try:
        claims = get_jwt()
    except:
        return "not authorized", 403
    return jsonify(claims), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_jwt():
    identity = get_jwt_identity()
    access_token = create_access_JWT(identity, True)
    response = jsonify({"msg": "refresh successful"}, 200)
    set_access_cookies(response, access_token)
    return response, 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    payload = get_jwt()
    jti = payload["jti"]
    token_type = payload["type"]
    try:
        token_blocklist = TokenBlocklist(jti=jti, token_type=token_type)
        current_user.is_authenticated = False
        db.session.add(token_blocklist)
        db.session.add(current_user)
        db.session.commit()
    except Exception as e:
        return "server error", 500
    response = jsonify({"msg": "logout successful"}, 200)
    unset_jwt_cookies(response)
    flash("successful logout")
    return response, 200
