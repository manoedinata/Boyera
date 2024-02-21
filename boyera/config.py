import os
from dotenv import dotenv_values

env = dotenv_values(".env")

ENV = os.environ.get("ENV")
if ENV:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MYSQL_URL = os.environ.get("MYSQL_URL")
else:
    SECRET_KEY = env.get("SECRET_KEY")
    MYSQL_URL = env.get("MYSQL_URL")

config = {
    "SECRET_KEY": SECRET_KEY,
    "MYSQL_URL": MYSQL_URL
}
