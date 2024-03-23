from flask import Flask

from flask_dance.contrib.azure import make_azure_blueprint

import os

from boyera import config
from boyera.database import db
from boyera.database import migrate

from boyera.auth import login_manager

def create_app() -> Flask:
    app = Flask(__name__)

    # Configurations
    app.secret_key = config.SECRET_KEY

    # OAuth: Allow to change the requested OAuth scopes
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    # Database (Flask-SQLAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URL
    db.init_app(app)
    migrate.init_app(app)

    # These need to be imported for Alembic migration
    from boyera.models.kelas import Jenjang, Kelas
    from boyera.models.siswa import Siswa, SiswaOAuth

    # Routes registration
    ## Frontend (Web UI)
    from boyera.routes.home import routes_home
    app.register_blueprint(routes_home)
    from boyera.routes.auth import routes_auth
    app.register_blueprint(routes_auth)
    from boyera.routes.auth import routes_dance
    app.register_blueprint(routes_dance, url_prefix="/oauth")
    from boyera.routes.profile import routes_profile
    app.register_blueprint(routes_profile)

    # Login manager (Flask-Login)
    login_manager.init_app(app)

    return app
