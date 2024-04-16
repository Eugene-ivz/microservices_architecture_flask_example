from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import exc, select

from app.extensions import db
from app.hashing import get_password_hash
from app.models import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/all")
@jwt_required()
def users_list():
    '''
    endpoint to get list of all users
    
    :return: list of all users in json
    
    '''
    users = db.session.scalars(select(User))
    return {"users": {str(user.id): user.username for user in users}}, 200


@users_bp.route("/create", methods=["POST"])
def create_user():
    '''
    endpoint to create new user via sqlalchemy
    
    :return: message and status code
    
    '''
    data = request.form
    try:
        user = User(
            username=request.form.get("username"),
            password=get_password_hash(request.form.get("password")),
            email=request.form.get("email"),
        )
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        return {"message": "User or email already exists"}, 409
    return "User created", 200


@users_bp.route("/whoami")
@jwt_required()
def user_details():
    '''
    endpoint to get user details via jwt claims
    
    '''
    return {"username": current_user.username, "email": current_user.email}, 200


@users_bp.route("/<uuid:id>/delete", methods=["DELETE"])
@jwt_required(fresh=True)
def user_delete(id):
    '''
    endpoint to delete user via sqlalchemy
    
    :param id: user id
    :return: message and status code
    
    '''
    user = db.get_or_404(User, id)

    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
