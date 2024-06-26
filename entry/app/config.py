class Config(object):
    TESTING = False
    # flask
    SECRET_KEY = "05f444452bc4405133dc91ba3a7aee6739a4709f6cc2daaa9f360e13b5354f3e"
    # mongo
    MONGO_URI = "mongodb://localhost:27050"
    MONGO_URI_PDF = "db_pdf"
    MONGO_URI_TXT = "db_txt"
    # rabbitmq
    RABBITMQ_HOST = "amqp://rabbitmq:5672"
    PDF_TO_TEXT_QUEUE = "pdf_to_text"
    TEXT_TO_CONSUMER_QUEUE = "text_to_consumer"
    # api
    AUTH_VALIDATE_JWT = "http://localhost:5010/auth/validate"
    AUTH_CREATE_JWT = "http://localhost:5010/auth/login"
    AUTH_LOGOUT = "http://localhost:5010/auth/logout"
    AUTH_USER_REGISTRATION = "http://localhost:5010//users/create"
    JWT_REFRESH_PATH = "/auth/refresh"
    


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    ENV = "production"
    AUTH_VALIDATE_JWT = "http://auth:5010/auth/validate"
    AUTH_CREATE_JWT = "http://auth:5010/auth/login"
    AUTH_LOGOUT = "http://auth:5010/auth/logout"
    AUTH_USER_REGISTRATION = "http://auth:5010//users/create"
    MONGO_URI = "mongodb://mongodb:27017"

class TestingConfig(DevelopmentConfig):
    ENV = "testing"
    TESTING = True
