from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from boyera.auth import oauth
from authlib.jose.errors import InvalidTokenError
from boyera.database import Siswa
from boyera.utils import getSiswaByEmail
from boyera.utils import addSiswa
import time

routes_auth = Blueprint("routes_auth", __name__, template_folder="templates", url_prefix="/")

@routes_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_home.home"))

    return render_template("routes/login.html")

@routes_auth.post("/login")
def redirect_login():
    redirect_uri = url_for("routes_auth.auth_callback", _external=True)
    return oauth.smaboy.authorize_redirect(redirect_uri)

@routes_auth.route("/auth")
def auth_callback():
    token = oauth.smaboy.authorize_access_token()

    siswa = Siswa()
    siswa.from_userinfo_callback(token["userinfo"])

    # cek apakah siswa sdh ada di db
    siswaAda = getSiswaByEmail(token["userinfo"]["preferred_username"])
    if not siswaAda:
        addSiswa(siswa)

    login_user(siswa, remember=True)
    return redirect(url_for("routes_home.home"))

@routes_auth.get("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Berhasil logout!", "success")

    return redirect(url_for("routes_auth.login"))
