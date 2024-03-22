from boyera.database import db

class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jam = db.Column(db.Integer)
    hari = db.Column(db.Integer)

    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    guru_id = db.Column(db.Integer, db.ForeignKey("guru.index"))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "jam": self.jam,
            "hari": self.hari,
            "kelas_id": self.kelas_id,
            "guru_id": self.guru_id,
        }

    def __repr__(self):
        return f'<Jadwal {self.kelas_id}>'
