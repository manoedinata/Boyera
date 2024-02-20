import os
from dotenv import dotenv_values

env = dotenv_values(".env")

ENV = os.environ.get("ENV")
if ENV:
    MYSQL_URL = os.environ.get("MYSQL_URL")
else:
    MYSQL_URL = env.get("MYSQL_URL")

config = {
    "MYSQL_URL": MYSQL_URL
}
