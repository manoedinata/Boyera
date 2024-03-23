from flask_login import UserMixin

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from base64 import b64encode

from boyera.database import db

class Siswa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(200), nullable=False, unique=False)
    nama = db.Column(db.String(1000), nullable=False, unique=False)
    email = db.Column(db.String(1000), nullable=False, unique=True)
    picture = db.Column(db.BLOB, nullable=True, unique=False)
    role = db.Column(db.String(100), nullable=True, unique=False, default="Siswa")

    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))

    def getPicture(self):
        if not self.picture:
            return None

        return b64encode(self.picture).decode()

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

class SiswaOAuth(OAuthConsumerMixin, db.Model):
    provider_siswa_id = db.Column(db.String(256), unique=True, nullable=False)
    siswa_id = db.Column(db.Integer, db.ForeignKey(Siswa.id))
    siswa = db.relationship(Siswa)
