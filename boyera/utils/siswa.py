from boyera.database import db
from boyera.database import Siswa

def getSiswaByUid(uid: str) -> Siswa:
    siswa = Siswa.query.filter_by(uid=uid).first()

    return siswa

def addSiswa(siswa: Siswa) -> Siswa:
    db.session.add(siswa)
    db.session.commit()

    return siswa

def editSiswa(siswa: Siswa, nama: str, email: str, picture) -> Siswa:
    siswa.nama = nama
    siswa.email = email
    siswa.picture = picture

    db.session.commit()

    return siswa
