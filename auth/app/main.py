import os
from datetime import UTC, datetime, timedelta

from flask import Flask
from flask_jwt_extended import get_jwt, get_jwt_identity, set_access_cookies
from sqlalchemy import select

from app.extensions import cors, db, jwt, migrate


def create_app(test_config=None) -> Flask:
    '''
    Create and configure an instance of the Flask application.
    
    :param test_config: A configuration dictionary for testing purposes.
    :return: An instance of the Flask application.
    '''
    app = Flask(__name__)
    app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
    if app.config["FLASK_ENV"] == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif app.config["FLASK_ENV"] == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif app.config["FLASK_ENV"] == "testing":
        app.config.from_object("app.config.TestingConfig")

    if test_config:
        app.config.update(test_config)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # blueprints
    from app.auth import auth_bp  # isort:skip

    app.register_blueprint(auth_bp)
    from app.users import users_bp  # isort:skip

    app.register_blueprint(users_bp)

    # jwt loaders
    from app.jwt_utils import create_access_JWT  # isort:skip
    from app.models import TokenBlocklist, User  # isort:skip

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        '''
        get user in protected jwt route
        
        '''
        identity = jwt_data["sub"]
        return db.session.scalar(select(User).where(User.username == identity))

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        '''
        check if token in blocklist
        
        '''
        jti = jwt_payload["jti"]
        token = db.session.scalar(
            select(TokenBlocklist).where(TokenBlocklist.jti == jti)
        )
        return token is not None

    @jwt.revoked_token_loader
    def is_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        '''
        if token in blocklist
        returns login error
        
        '''
        return "Need to login", 401

    @jwt.needs_fresh_token_loader
    def need_fresh_token_callback(jwt_header, jwt_payload):
        '''
        check freshness of token
        
        '''
        return "need fresh login", 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        '''
        check if token expired
        
        '''
        return "Need to login", 401

    # refresh jwt token before expiration after request
    @app.after_request
    def refresh_expiring_jwts(response):
        '''
        refresh jwt token before expiration after request
        
        '''
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(UTC)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
            if target_timestamp > exp_timestamp:
                access_token = create_access_JWT(get_jwt_identity(), True)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5010)
