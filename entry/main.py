from flask import Flask, render_template


def create_app():
    # flask
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
    from entry.extensions import csrf, mongo # isort:skip
    # global csrf
    csrf.init_app(app)
    # # pymongo 
    mongo.init_app(app)   
    
    from entry.converter import converter_bp # isort:skip
    app.register_blueprint(converter_bp)
    from entry.auth import auth_bp # isort:skip
    app.register_blueprint(auth_bp)
        
    @app.route('/')
    def index():
        ctx = {'msg' :'START PAGE'}
        return render_template('index.html', **ctx)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8090, debug=True)
