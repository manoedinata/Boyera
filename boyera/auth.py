from flask_login import LoginManager

from boyera.utils import getSiswaByNis

login_manager = LoginManager()
login_manager.login_view = "routes_auth.login"
login_manager.login_message = ""

@login_manager.user_loader
def load_user(user_id):
    # user_id = nis
    return getSiswaByNis(user_id)
