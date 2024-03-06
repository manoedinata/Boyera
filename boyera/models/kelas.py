from boyera.database import db
from boyera.models.siswa import Siswa

class Jenjang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jenjang = db.Column(db.String(100), nullable=False, unique=True)
    kelas = db.relationship("Kelas", backref="jenjang")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/11884806"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Jenjang {self.jenjang}>"

class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kelas = db.Column(db.String(100), nullable=False, unique=True)
    jenjang_id = db.Column(db.Integer, db.ForeignKey("jenjang.id"))
    siswa = db.relationship("Siswa", backref="kelas")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/11884806"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Kelas {self.kelas}>"
