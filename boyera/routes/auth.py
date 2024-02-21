from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from boyera.utils import getSiswaByNis

routes_auth = Blueprint("routes_auth", __name__, template_folder="templates", url_prefix="/")

@routes_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_home.home"))

    return render_template("routes/login.html")

@routes_auth.post("/login")
def process_login():
    nis = request.form.get("nis")
    siswa = getSiswaByNis(nis)

    if not siswa:
        flash("Akun tidak ditemukan! Cek kembali NIS Anda.", "danger")
        return redirect(url_for("routes_auth.login"))

    login_user(siswa, remember=True)
    return redirect(url_for("routes_home.home"))

@routes_auth.get("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Berhasil logout!", "success")

    return redirect(url_for("routes_auth.login"))
