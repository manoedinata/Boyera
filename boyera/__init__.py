from flask import Flask

from boyera.config import config
from boyera.database import db
from boyera.database import migrate

from boyera.auth import login_manager

from boyera.routes import routes_home
from boyera.routes import routes_auth

def create_app() -> Flask:
    app = Flask(__name__)

    # Configurations
    app.config.update(**config)
    app.secret_key = app.config["SECRET_KEY"]

    # Database (Flask-SQLAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["MYSQL_URL"]
    db.init_app(app)
    migrate.init_app(app)

    # Routes registration
    ## Frontend (Web UI)
    app.register_blueprint(routes_home)
    app.register_blueprint(routes_auth)

    # Login manager (Flask-Login)
    login_manager.init_app(app)

    return app
