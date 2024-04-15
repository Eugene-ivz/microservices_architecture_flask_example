from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from app.auth_utils import add_auth_cookies, create_user, get_jwt, logout_user
from app.forms import User_login_form, User_registration_form

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/registration", methods=["GET", "POST"])
def user_registration():
    form = User_registration_form()
    if form.validate_on_submit():
        error = create_user(request)
        if not error:
            flash("Thanks for registering")
            return redirect(url_for("auth.login"), 303)
    return render_template("auth/registration.html", form=form)


# get jwt token from auth service
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = User_login_form()
    if form.validate_on_submit():
        cookies, error = get_jwt(request)
        if not error:
            response = make_response(redirect(url_for("index"), 303))
            response = add_auth_cookies(response, cookies)
            return response
        else:
            flash(error)
        return redirect(url_for("index"), 303)
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
def logout():
    ok, error = logout_user(request)
    if error:
        flash("Need to login first")
        return redirect(url_for("index"), 303)
    else:
        flash("successful logout")
        return redirect(url_for("index"), 303)
