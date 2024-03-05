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

from oauthlib.oauth2 import WebApplicationClient
import requests
import json

from boyera.database import Siswa
from boyera.utils.siswa import getSiswaByUid
from boyera.utils.siswa import addSiswa
from boyera.utils.siswa import editSiswa
from boyera.utils.datetime import addTimeBySeconds

from boyera import config

routes_auth = Blueprint("routes_auth", __name__, template_folder="templates", url_prefix="/")

@routes_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_home.home"))

    return render_template("routes/login.html")

@routes_auth.post("/login")
def redirect_login():
    # OAuth client
    oauth_client = WebApplicationClient(config.SSO_CLIENT_ID)

    # Use library to construct the request for Microsoft login and provide
    # scopes that let you retrieve user's profile from Microsoft
    request_uri = oauth_client.prepare_request_uri(
        config.SSO_AUTHORIZE_ENDPOINT,
        redirect_uri=url_for("routes_auth.auth_callback", _external=True),
        scope=["openid", "profile", "email", "User.Read"],
    )
    return redirect(request_uri)

@routes_auth.route("/auth")
def auth_callback():
    # OAuth client
    oauth_client = WebApplicationClient(config.SSO_CLIENT_ID)

    # Get authorization code Microsoft sent back
    code = request.args.get("code")

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = oauth_client.prepare_token_request(
        config.SSO_TOKEN_ENDPOINT,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config.SSO_CLIENT_ID, config.SSO_CLIENT_SECRET),
    ).json()

    # Parse the tokens!
    oauth_client.parse_request_body_response(json.dumps(token_response))

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

    # cek apakah siswa sdh ada di db
    siswa = getSiswaByUid(uid)
    if siswa:
        siswa = editSiswa(siswa, nama=nama, email=email, picture=picture)
    else:
        siswa = Siswa(uid=uid, nama=nama, email=email, picture=picture)
        addSiswa(siswa)

    # Get token expiration
    tokenExpire = addTimeBySeconds(token_response["expires_in"])

    session["access_token"] = oauth_client.access_token
    session["expires_in"] = tokenExpire
    login_user(siswa, remember=True)

    return redirect(url_for("routes_home.home"))

@routes_auth.get("/logout")
def logout():
    if session.get("access_token"):
        session.pop("access_token")
    if session.get("expires_in"):
        session.pop("expires_in")

    logout_user()

    flash("Berhasil logout!", "success")
    return redirect(url_for("routes_auth.login"))
