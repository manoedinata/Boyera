from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db=db)

class Siswa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.Integer, nullable=False, unique=True)
    nama = db.Column(db.String(1000), nullable=False, unique=False)
    jenjang = db.Column(db.Integer, nullable=False, unique=False)
    kelas = db.Column(db.String(100), nullable=False, unique=False)

    # Override UserMixin `get_id()`
    def get_id(self):
        return str(self.nis)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "nis": self.nis,
            "name": self.nama,
            "jenjang": self.jenjang,
            "kelas": self.kelas
        }

    def __repr__(self):
        return f"<Siswa {self.nis}>"
