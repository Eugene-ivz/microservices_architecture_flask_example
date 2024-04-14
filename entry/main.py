from flask import Flask, render_template
from entry.extensions import csrf, mongo

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
    

    csrf.init_app(app)

    mongo.init_app(app)

    from entry.converter import converter_bp  # isort:skip

    app.register_blueprint(converter_bp)
    from entry.auth import auth_bp  # isort:skip

    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        ctx = {"msg": "START PAGE"}
        return render_template("index.html", **ctx)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
