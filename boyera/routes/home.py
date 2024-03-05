from flask import Blueprint
from flask import render_template

from flask_login import current_user
from flask_login import login_required

routes_home = Blueprint("routes_home", __name__, template_folder="templates", url_prefix="/")

@routes_home.get("/")
@login_required
def home():
    print(current_user.serialize)
    return render_template("routes/home.html")
