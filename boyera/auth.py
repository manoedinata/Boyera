from flask import session

from flask_login import LoginManager

from boyera.utils import getSiswaByEmail
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

login_manager = LoginManager()
login_manager.login_view = "routes_auth.login"
login_manager.login_message = ""

@login_manager.user_loader
def load_user(user_id):
    return getSiswaByEmail(user_id)
