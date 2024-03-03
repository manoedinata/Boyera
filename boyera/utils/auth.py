import requests

from boyera.config import SSO_OPENID_CONFIG

def get_provider_cfg() -> dict:
    return requests.get(SSO_OPENID_CONFIG).json()
