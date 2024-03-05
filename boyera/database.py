from flask import session

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_migrate import Migrate

from base64 import b64encode

from boyera.utils.datetime import getCurrentTime

db = SQLAlchemy()
migrate = Migrate(db=db)

class Siswa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, unique=False)
    nama = db.Column(db.String(1000), nullable=False, unique=False)
    email = db.Column(db.String(1000), nullable=False, unique=True)
    picture = db.Column(db.BLOB, nullable=True, unique=False)
    role = db.Column(db.String(100), nullable=True, unique=False, default="Siswa")

    def getPicture(self):
        if not self.picture:
            return None

        return b64encode(self.picture).decode()

    # Override UserMixin `is_active()`
    @property
    def is_active(self):
        if not (session.get("access_token") and session.get("expires_in")):
            return False

        # Cek apakah token masih valid
        currentDate = getCurrentTime()
        if session.get("expires_in") < currentDate:
            return False

        return True

    # Override UserMixin `get_id()`
    def get_id(self):
        return str(self.uid)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "uid": self.uid,
            "nama": self.nama,
            "email": self.email,
            "picture": b64encode(self.picture).decode() if self.picture else None,
            "role": self.role
        }

    def __repr__(self):
        return f"<Siswa {self.nama}>"
