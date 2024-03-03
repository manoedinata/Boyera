from flask import session

from flask_login import LoginManager

from boyera.utils.siswa import getSiswaByUid

# Flask-Login login manager
login_manager = LoginManager()
login_manager.login_view = "routes_auth.login"
login_manager.login_message = ""

@login_manager.user_loader
def load_user(user_id):
    siswa = getSiswaByUid(user_id)

    if siswa:
        siswa.access_token = session.get("access_token")

    return siswa
