from boyera.database import db
from boyera.models.kelas import Jenjang

def addJenjang(jenjang: str):
    cek = Jenjang.query.filter_by(jenjang=jenjang).first()
    if cek:
        return cek

    add = Jenjang(jenjang=jenjang)
    db.session.add(add)
    db.session.commit()

    return add

def getJenjang():
    jenjang = Jenjang.query.all()

    return [j for j in jenjang]
