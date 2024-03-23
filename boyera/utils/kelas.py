from boyera.database import db
from boyera.models.kelas import Kelas
from boyera.models.siswa import Siswa

def getKelas():
    kelas = Kelas.query.all()

    return [k for k in kelas]

def addKelas(kelas: str, jenjang_id: int):
    cek = Kelas.query.filter_by(kelas=kelas).first()
    if cek:
        return cek

    add = Kelas(kelas=kelas, jenjang_id=jenjang_id)
    db.session.add(add)
    db.session.commit()

    return add

def editKelas(siswa: Siswa, kelas: str) -> Siswa:
    kelas = Kelas.query.filter_by(kelas=kelas).first()

    siswa.kelas_id = kelas.id

    db.session.add(kelas)
    db.session.commit()

    return siswa
