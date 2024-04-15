import os

from flask import Flask, render_template

from app.extensions import csrf, mongo


def create_app(test_config=None) -> Flask:
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

    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

    csrf.init_app(app)

    mongo.init_app(app)

    from app.converter import converter_bp  # isort:skip

    app.register_blueprint(converter_bp)

    from app.auth import auth_bp  # isort:skip

    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        ctx = {"msg": "START PAGE"}
        return render_template("index.html", **ctx)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
