from typing import Optional

import requests
from oauthlib.oauth2 import WebApplicationClient

from flask_login import current_user

from boyera.config import SSO_CLIENT_ID

def getProfilePic(access_token: str, oauth_client: Optional[WebApplicationClient] = None, client_id: str = SSO_CLIENT_ID):
    if not oauth_client:
        oauth_client = WebApplicationClient(client_id=client_id, access_token=access_token)

    picture_endpoint = "https://graph.microsoft.com/v1.0/me/photo/$value"
    uri, headers, body = oauth_client.add_token(picture_endpoint)
    picture_response = requests.get(uri, headers=headers, data=body)

    return picture_response
