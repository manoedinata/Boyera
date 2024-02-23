from boyera.database import db
from boyera.database import Siswa

def getSiswaByEmail(email: str) -> Siswa:
    siswa = Siswa.query.filter_by(email=email).first()

    return siswa

def addSiswa(siswa: Siswa):
    db.session.add(siswa)
    db.session.commit()
