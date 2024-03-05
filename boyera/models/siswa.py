from flask import session

from flask_login import UserMixin

from base64 import b64encode

from boyera.database import db
from boyera.utils.datetime import getCurrentTime

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
        """https://stackoverflow.com/a/11884806"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Siswa {self.nama}>"
