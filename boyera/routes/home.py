from flask import Blueprint
from flask import render_template

from flask_login import login_required

routes_home = Blueprint("routes_home", __name__, template_folder="templates", url_prefix="/")

@routes_home.get("/")
@login_required
def home():
    return render_template("routes/base.html")
