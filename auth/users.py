from flask import Blueprint, jsonify, redirect, request, url_for
from sqlalchemy import select, exc

from auth.extensions import db


from flask_jwt_extended import current_user, jwt_required

from auth.hashing import get_password_hash
from auth.models import User


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/all")
@jwt_required()
def users_list():
    users = db.session.scalars(select(User))
    return {"users": {str(user.id):user.username for user in users}}, 200


@users_bp.route("/create", methods=["POST"])
def create_user():
    data = request.form
    try:
        user = User(
            username=request.form.get("username"),
            password=get_password_hash(request.form.get("password")),
            email=request.form.get("email")
        )
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        return {"message": "User or email already exists"}, 409
    return "User created", 200



@users_bp.route("/<uuid:id>")
@jwt_required()
def user_details(id):
    return {'username': current_user.username,
            'email': current_user.email}, 200


@users_bp.route("/<uuid:id>/delete", methods=['DELETE'])
@jwt_required(fresh=True)
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
    

