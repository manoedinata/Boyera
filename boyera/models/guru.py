from boyera.database import db

class Guru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=True)
    nama = db.Column(db.String(255))
    mapel = db.Column(db.String(255))

    jadwal = db.relationship("Jadwal", backref="guru")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "index": self.index,
            "nama": self.nama,
            "mapel": self.mapel
        }

    def __repr__(self):
        return f'<Guru {self.nama}>'
