from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class User_registration_form(FlaskForm):
    '''
    form for user registration
    
    '''
    username = StringField(
        "Username", validators=[DataRequired(message="username required")]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="password required"),
        ],
    )
    confirm = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(message="password required"),
            EqualTo("password", message="Password must match"),
        ],
    )
    email = EmailField(
        "Email (optional)", validators=[DataRequired(message="email required"), Email()]
    )


class User_login_form(FlaskForm):
    '''
    form for user login
    
    '''
    username = StringField(
        "Username", validators=[DataRequired(message="username required")]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="password required"),
        ],
    )


class File_upload_form(FlaskForm):
    '''
    form for file upload
    
    '''
    file = FileField(
        "file",
        validators=[
            DataRequired(message="file required"),
            FileAllowed(["pdf"], "PDF only!"),
        ],
    )
    submit = SubmitField("Submit")


class File_download_form(FlaskForm):
    '''
    form for file download
    
    '''
    text_id = StringField(
        "text_id",
        validators=[
            DataRequired(message="text_id required"),
            Regexp(r"[a-zA-Z0-9]+", message="text_id must be alphanumeric"),
        ],
    )
