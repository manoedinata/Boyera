from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.azure import make_azure_blueprint
from flask_dance.consumer import oauth_authorized

from boyera.database import db

from boyera.models.siswa import Siswa
from boyera.models.siswa import SiswaOAuth
from boyera.utils.siswa import getSiswaByUid
from boyera.utils.siswa import addSiswa

from boyera import config

routes_auth = Blueprint("routes_auth", __name__, template_folder="templates", url_prefix="/")
routes_dance = make_azure_blueprint(
    config.SSO_CLIENT_ID,
    config.SSO_CLIENT_SECRET,
    scope=["openid", "profile", "email", "offline_access", "User.Read"],
    tenant=config.SSO_TENANT
)
routes_dance.storage = SQLAlchemyStorage(SiswaOAuth, db.session, user=current_user)

@routes_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_home.home"))

    return render_template("routes/login.html")

@routes_auth.post("/login")
def redirect_login():
    return redirect(url_for("azure.login"))

@oauth_authorized.connect_via(routes_dance)
def auth_callback(blueprint, token):
    if not token:
        flash("Gagal login, harap coba lagi.", "danger")
        return redirect(url_for("routes_auth.login"))

    userinfo_response = blueprint.session.get(config.SSO_USERINFO_ENDPOINT)
    if not userinfo_response.ok:
        flash("Gagal memproses data, harap laporkan Admin.", "danger")
        return redirect(url_for("routes_auth.login"))

    info = userinfo_response.json()
    uid = info["sub"]
    email = info["email"]
    nama = info["name"]

    picture = None
    picture_response = blueprint.session.get(config.SSO_PICTURE_ENDPOINT)
    if picture_response.ok:
        picture = picture_response.content

    # Cek apakah siswa sudah ada di db
    siswaOauth = SiswaOAuth.query.filter_by(provider=blueprint.name, provider_siswa_id=uid).first()
    if not siswaOauth:
        siswaOauth = SiswaOAuth(provider=blueprint.name, provider_siswa_id=uid, token=token)

    if not siswaOauth.siswa:
        siswa = getSiswaByUid(uid)
        if not siswa:
            # Buat akun
            siswa = Siswa(uid=uid, nama=nama, email=email, picture=picture)
            siswa = addSiswa(siswa)

        # Hubungkan Siswa ke SiswaOauth
        siswaOauth.siswa = siswa

        db.session.add(siswaOauth)
        db.session.commit()

    login_user(siswaOauth.siswa)

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

@routes_auth.get("/logout")
def logout():
    logout_user()

    flash("Berhasil logout!", "success")
    return redirect(url_for("routes_auth.login"))
