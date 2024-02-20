from flask import Flask

from boyera.routes import routes_home

def create_app() -> Flask:
    app = Flask(__name__)

    # Routes registration
    ## Frontend (Web UI)
    app.register_blueprint(routes_home)

    return app
