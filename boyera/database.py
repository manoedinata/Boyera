from flask import session

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db=db)

class Siswa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, unique=False)
    nama = db.Column(db.String(1000), nullable=False, unique=False)
    email = db.Column(db.String(1000), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=True, unique=False, default="Siswa")

    # Override UserMixin `is_active()`
    @property
    def is_active(self):
        if not session.get("access_token"):
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
            "nama": self.nama,
            "email": self.email,
            "role": self.role
        }

    def __repr__(self):
        return f"<Siswa {self.nama}>"
