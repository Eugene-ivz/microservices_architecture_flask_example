
class Config(object):
    TESTING = False
    # flask
    SECRET_KEY = "05f444452bc4405133dc91ba3a7aee6739a4709f6cc2daaa9f360e13b5354f3e"
    APP = "main.py"
    # mongo
    MONGO_URI = "mongodb://localhost:27017"
    MONGO_URI_PDF = "db_pdf"
    MONGO_URI_TXT = "db_txt"
    # rabbitmq
    RABBITMQ_HOST = "amqp://guest:guest@host.docker.internal:5672"
    PDF_TO_TEXT_QUEUE = "pdf_to_text"
    TEXT_TO_CONSUMER_QUEUE = "text_to_consumer"
    # api
    AUTH_VALIDATE_JWT = "localhost:5000/auth/validate"
    AUTH_CREATE_JWT = "localhost:5000/auth/login"
    AUTH_LOGOUT = "localhost:5000/auth/logout"
    AUTH_USER_REGISTRATION = "localhost:5000//users/create"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    ENV = "production"


class TestingConfig(DevelopmentConfig):
    ENV = "testing"
    TESTING = True
