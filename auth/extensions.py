from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_cors import CORS

# cors
cors = CORS()

# flask-sqlalchemy
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base, add_models_to_shell=True)

# flask-migrate
migrate = Migrate()

# flask-jwt-extended
jwt = JWTManager()





