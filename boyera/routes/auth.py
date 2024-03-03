from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

import requests
import json

from oauthlib.oauth2 import WebApplicationClient
from boyera.utils.auth import get_provider_cfg

from boyera.database import Siswa
from boyera.utils.siswa import getSiswaByUid
from boyera.utils.siswa import addSiswa
from boyera.utils.siswa import editSiswa

from boyera.config import SSO_CLIENT_ID
from boyera.config import SSO_CLIENT_SECRET

routes_auth = Blueprint("routes_auth", __name__, template_folder="templates", url_prefix="/")

@routes_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_home.home"))

    return render_template("routes/login.html")

@routes_auth.post("/login")
def redirect_login():
    # OAuth client
    oauth_client = WebApplicationClient(SSO_CLIENT_ID)

    provider_cfg = get_provider_cfg()
    authorization_endpoint = provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Microsoft login and provide
    # scopes that let you retrieve user's profile from Microsoft
    request_uri = oauth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("routes_auth.auth_callback", _external=True),
        scope=["openid", "profile", "email", "User.Read"],
    )
    return redirect(request_uri)

@routes_auth.route("/auth")
def auth_callback():
    # OAuth client
    oauth_client = WebApplicationClient(SSO_CLIENT_ID)

    # Get authorization code Microsoft sent back
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    provider_cfg = get_provider_cfg()
    token_endpoint = provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(SSO_CLIENT_ID, SSO_CLIENT_SECRET),
    ).json()

    # Parse the tokens!
    oauth_client.parse_request_body_response(json.dumps(token_response))

    # Now that we have tokens let's retrieve user's profile information
    userinfo_endpoint = provider_cfg["userinfo_endpoint"]
    uri, headers, body = oauth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    # Parse userinfo data
    uid = userinfo_response["sub"]
    email = userinfo_response["email"]
    nama = userinfo_response["name"]

    # cek apakah siswa sdh ada di db
    siswa = getSiswaByUid(uid)
    if siswa:
        siswa = editSiswa(siswa, nama=nama, email=email)
    else:
        siswa = Siswa(uid=uid, nama=nama, email=email)
        addSiswa(siswa)

    session["access_token"] = oauth_client.access_token
    login_user(siswa, remember=True)

    return redirect(url_for("routes_home.home"))

@routes_auth.get("/logout")
def logout():
    session.pop("access_token")
    logout_user()

    flash("Berhasil logout!", "success")
    return redirect(url_for("routes_auth.login"))
