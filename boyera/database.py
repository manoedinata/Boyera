from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db=db)

class Siswa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(1000), nullable=False, unique=False)
    email = db.Column(db.String(1000), nullable=False, unique=True)
    jenjang = db.Column(db.Integer, nullable=True, unique=False)
    kelas = db.Column(db.String(100), nullable=True, unique=False)
    role = db.Column(db.String(100), nullable=True, unique=False, default="Siswa")

    # Override UserMixin `get_id()`
    def get_id(self):
        return str(self.email)

    # Insert data from userinfo JSON response
    def from_userinfo_callback(self, userinfo: dict):
        self.nama = userinfo["name"]
        self.email = userinfo["email"]

        return self

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "nama": self.nama,
            "email": self.email,
            "jenjang": self.jenjang,
            "kelas": self.kelas,
            "role": self.role
        }

    def __repr__(self):
        return f"<Siswa {self.nama}>"
