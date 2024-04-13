from bson import Regex
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Regexp
from flask_wtf.file import FileField, FileAllowed


class User_registration_form(FlaskForm):
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
    email = EmailField("Email (optional)", validators=[Optional(), Email()])


class User_login_form(FlaskForm):
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
    file = FileField(
        "file",
        validators=[
            DataRequired(message="file required"),
            FileAllowed(["pdf"], "PDF only!"),
        ],
    )
    submit = SubmitField("Submit")


class File_download_form(FlaskForm):
    text_id = StringField(
        "text_id",
        validators=[
            DataRequired(message="text_id required"),
            Regexp(r"[a-zA-Z0-9]+", message="text_id must be alphanumeric"),
        ],
    )
