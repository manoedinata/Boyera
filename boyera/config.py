import os
from dotenv import dotenv_values

env = dotenv_values(".env")

ENV = os.environ.get("ENV")
if ENV:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MYSQL_URL = os.environ.get("MYSQL_URL")
    SSO_TENANT = os.environ.get("SSO_TENANT")
    SSO_CLIENT_ID = os.environ.get("SSO_CLIENT_ID")
    SSO_CLIENT_SECRET = os.environ.get("SSO_CLIENT_SECRET")
else:
    SECRET_KEY = env.get("SECRET_KEY")
    MYSQL_URL = env.get("MYSQL_URL")
    SSO_TENANT = env.get("SSO_TENANT")
    SSO_CLIENT_ID = env.get("SSO_CLIENT_ID")
    SSO_CLIENT_SECRET = env.get("SSO_CLIENT_SECRET")

SSO_AUTHORIZE_ENDPOINT = f"https://login.microsoftonline.com/{SSO_TENANT}/oauth2/v2.0/authorize"
SSO_TOKEN_ENDPOINT = f"https://login.microsoftonline.com/{SSO_TENANT}/oauth2/v2.0/token"
SSO_USERINFO_ENDPOINT = "https://graph.microsoft.com/oidc/userinfo"

config = {
    "SECRET_KEY": SECRET_KEY,
    "MYSQL_URL": MYSQL_URL,
    "SSO_TENANT": SSO_TENANT,
    "SSO_CLIENT_ID": SSO_CLIENT_ID,
    "SSO_CLIENT_SECRET": SSO_CLIENT_SECRET
}
