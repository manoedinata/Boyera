from boyera.database import db
from boyera.models.kelas import Jenjang, Kelas
from boyera.models.siswa import Siswa

def getKelas():
    kelas = Kelas.query.all()

    return [k for k in kelas]

def getJenjang():
    jenjang = Jenjang.query.all()

    return [j for j in jenjang]

def editKelas(siswa: Siswa, kelas: str) -> Siswa:
    kelas = Kelas.query.filter_by(kelas=kelas).first()

    siswa.kelas_id = kelas.id

    db.session.add(kelas)
    db.session.commit()

    return siswa
