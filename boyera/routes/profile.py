from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_required
from flask_login import current_user

import requests
from oauthlib.oauth2 import WebApplicationClient

from boyera import config
from boyera.utils.siswa import editSiswa
from boyera.utils.kelas import getJenjang
from boyera.utils.kelas import editKelas

routes_profile = Blueprint("routes_profile", __name__, template_folder="templates", url_prefix="/profil")

@routes_profile.get("/")
@login_required
def profile():
    return render_template("routes/profile/profile.html")

@routes_profile.get("/kelas")
@login_required
def kelas():
    jenjang = getJenjang()
    return render_template("routes/profile/kelas.html", jenjang=jenjang)

@routes_profile.post("/kelas")
@login_required
def edit_kelas():
    kelas = request.form.get("kelas")
    editKelas(current_user, kelas)

    return redirect(url_for("routes_profile.kelas"))

@routes_profile.get("/sinkronisasi")
@login_required
def sync_profile():
    oauth_client = WebApplicationClient(config.SSO_CLIENT_ID, access_token=current_user.access_token)

    # Now that we have tokens let's retrieve user's profile information
    uri, headers, body = oauth_client.add_token(config.SSO_USERINFO_ENDPOINT)
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    # Get user picture
    picture_endpoint = userinfo_response["picture"]
    uri, headers, body = oauth_client.add_token(picture_endpoint)
    picture_response = requests.get(uri, headers=headers, data=body)

    # Parse userinfo data
    uid = userinfo_response["sub"]
    email = userinfo_response["email"]
    nama = userinfo_response["name"]
    picture = picture_response.content

    # Update user data
    siswa = current_user
    siswa = editSiswa(siswa=siswa, nama=nama, email=email, picture=picture)

    flash("Berhasil memperbarui data akun. Silahkan login kembali.", "success")
    return redirect(url_for("routes_auth.logout"))
