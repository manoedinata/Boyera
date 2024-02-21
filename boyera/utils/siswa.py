from boyera.database import db
from boyera.database import Siswa

def getSiswaByNis(nis: int) -> Siswa:
    siswa = Siswa.query.filter_by(nis=nis).first()

    return siswa

def addSiswa(nis: int, nama: str, jenjang: int, kelas: str):
    siswa = Siswa(
        nis=nis,
        nama=nama,
        jenjang=jenjang,
        kelas=kelas
    )

    db.session.add(siswa)
    db.session.commit()
