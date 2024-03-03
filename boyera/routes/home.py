from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from boyera.utils.msgraph import getProfilePic
from base64 import b64encode

routes_home = Blueprint("routes_home", __name__, template_folder="templates", url_prefix="/")

@routes_home.context_processor
def inject_dict_for_all_templates():
    # Profile image
    getPicture = getProfilePic(current_user.access_token)
    picture = b64encode(getPicture.content).decode()

    return {
        "picture": picture
    }

@routes_home.get("/")
@login_required
def home():
    return render_template("routes/home.html")
