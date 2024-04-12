import os
from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for, Response
from entry.auth_utils import create_user, get_jwt, logout_user, validate_jwt
from entry.forms import User_login_form, User_registration_form


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/registration', methods=['GET', 'POST'])
def user_registration():
    form = User_registration_form()
    if form.validate_on_submit():
        error = create_user(request)
        if not error:
            flash('Thanks for registering')
            return redirect(url_for('login'), 303)
    return render_template('auth/registration.html', form=form)
    


#get jwt token from auth service
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = User_login_form()
    if form.validate_on_submit():
        cookies, error = get_jwt(request)
        if not error:
            response = make_response(redirect(url_for('index'), 303))
            #response.headers['access_token_cookie']=resp.headers['access_token_cookie']
            #resp  = Response(response=response.content, status=response.status_code, headers=response.headers.items())
            # #TODO set cookie from cookies dict
            #print(cookies.json())
            response.set_cookie("access_token_cookie", cookies.get('access_token_cookie'),
                                httponly=True, secure=True, samesite='none')
            response.set_cookie("refresh_token_cookie", cookies.get('refresh_token_cookie'),
                                httponly=True, secure=True, samesite='none', path=os.getenv('FLASK_REFRESH'))
            response.set_cookie("csrf_access_token", cookies.get('csrf_access_token'),
                                secure=True, samesite='none')
            response.set_cookie("csrf_refresh_token", cookies.get('csrf_refresh_token'),
                                secure=True, samesite='none', path=os.getenv('FLASK_REFRESH'))
            return response
        else:
            flash(error)
        return redirect(url_for('index'), 303)
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    payload, error = logout_user(request)
    #user = payload.get(['sub']) 
    if error:
        flash('Need to login first')
        return redirect(url_for('index'), 303)
    else:
        flash('successful logout')
        return redirect(url_for('index'), 303)
        

@auth_bp.route('/delete', methods=['DELETE'])
def delete_user():
    pass