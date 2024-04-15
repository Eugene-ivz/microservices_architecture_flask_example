from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

cors = CORS()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, add_models_to_shell=True)

migrate = Migrate()

jwt = JWTManager()
