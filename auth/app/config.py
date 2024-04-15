from re import DEBUG


class Config(object):
    TESTING = False


class DevelopmentConfig(Config):
    ENV = "development"
    # flask
    DEBUG = True
    SECRET_KEY = "05f444452bc4405133dc91ba3a7aee6739a4709f6cc2daaa9f360e13b5354f3e"
    FLASK_APP = "main.py"
    # db
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg://postgres:postgres@localhost:5555/users"
    )
    DB_CONNINFO = "postgresql://postgres:postgres@localhost:5555/users"
    DB_NAME = "users"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5555
    # jwt
    JWT_SECRET_KEY = "dev"
    JWT_REFRESH_ADR = "http://localhost:5000/auth/refresh"
    JWT_TOKEN_LOCATION = "cookies"
    JWT_COOKIE_SECURE = True
    JWT_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_REFRESH_CSRF_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_SAMESITE = "none"
    JWT_CSRF_CHECK_FORM = True
    # cors
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ORIGINS = ["http://127.0.0.1:5001", "http://127.0.0.1:5000"]


class ProductionConfig(Config):
    ENV = "production"


class TestingConfig(DevelopmentConfig):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg://postgres:postgres@localhost:5556/test_users"
    )
