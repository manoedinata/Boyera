from typing import Union

from boyera.database import db
from boyera.models.guru import Guru

def listGuru(guru_id: Union[int, None] = None, mapel: Union[str, None] = None) -> list:
    guruQuery = Guru.query

    if guru_id:
        guru = guruQuery.filter_by(index=guru_id).first()
        if not guru:
            return {"message": f"Guru {guru_id} tidak ditemukan"}, 404

        return guru.serialize

    elif mapel:
        guruQuery = guruQuery.filter_by(mapel=mapel)

    return [guru.serialize for guru in guruQuery.all()]

def addGuru(index: int, nama: str, mapel: str) -> dict:
    guru = Guru(
        index=index,
        nama=nama,
        mapel=mapel
    )

    try:
        db.session.add(guru)
        db.session.commit()
        return guru.serialize
    except Exception as e:
        return {"message": str(e)}, 500
