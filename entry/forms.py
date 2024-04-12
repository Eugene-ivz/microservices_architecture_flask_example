from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class User_registration_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='username required')])
    password = PasswordField('Password', validators=[
        DataRequired(message='password required'),
        
        ])
    confirm  = PasswordField('Repeat Password', validators=[
        DataRequired(message='password required'),
        EqualTo('password', message='Password must match'),
        ])
    email = EmailField('Email (optional)',validators=[Optional(), Email()])
    
class User_login_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='username required')])
    password = PasswordField('Password', validators=[DataRequired(message='password required'),])