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

routes_jadwal = Blueprint("routes_jadwal", __name__, template_folder="templates", url_prefix="/jadwal")

@routes_jadwal.get("/")
@login_required
def jadwal():
    return render_template("routes/jadwal.html")
