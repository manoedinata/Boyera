from flask import Flask

from boyera.config import config
from boyera.database import db
from boyera.database import migrate

from boyera.routes import routes_home

def create_app() -> Flask:
    app = Flask(__name__)

    # Configurations
    app.config.update(**config)

    # Database (Flask-SQLAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["MYSQL_URL"]
    db.init_app(app)
    migrate.init_app(app)

    # Routes registration
    ## Frontend (Web UI)
    app.register_blueprint(routes_home)

    return app
