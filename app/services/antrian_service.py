from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.antrian_bimbingan import AntrianBimbingan
from app.schemas.antrian_bimbingan import AntrianBimbinganSchema

from app.models.waktu_bimbingan import WaktuBimbingan

from datetime import datetime

def create_antrian(db: Session, antrian: AntrianBimbinganSchema):
    db_antrian = AntrianBimbingan(**antrian.model_dump())
    db.add(db_antrian)
    db.commit()
    db.refresh(db_antrian)
    return db_antrian

def get_antrian_by_id(db: Session, id_antrian: int):
    return db.query(AntrianBimbingan).filter_by(AntrianBimbingan.id_antrian == id_antrian).first()

def ambil_antrian_bimbingan(db: Session, nim: str, waktu_id: int):
    waktu = db.query(WaktuBimbingan).filter_by(id=waktu_id).first()
    if not waktu:
        raise HTTPException(
            status_code=404,
            detail="Waktu bimbingan tidak ditemukan."
        )
    
    dosen = waktu.dosen
    if not dosen.ketersediaan_bimbingan:
        raise HTTPException(
            status_code=400,
            detail="Dosen tidak tersedia untuk bimbingan."
        )
    
    sudah_ada = db.query(AntrianBimbingan).filter_by(nim=nim, waktu_id=waktu_id).first()
    if sudah_ada:
        raise HTTPException(
            status_code=400,
            detail="Anda sudah masuk antrian."
        )
    
    jumlah = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).count()
    if jumlah >= waktu.jumlah_bimbingan:
        raise HTTPException(
            status_code=400,
            detail="Slot penuh."
        )
    
    antrian = AntrianBimbingan(
        nim = nim,
        waktu_id = waktu_id,
        nomor_induk = waktu.nomor_induk,
        status_antrian = "Menunggu",
        waktu_antrian = datetime.now()
    )
    db.add(antrian)
    db.commit()
    db.refresh(antrian)



    daftar = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).order_by(AntrianBimbingan.waktu_antrian).all()
    posisi = next((
        i+1 for i, m in enumerate(daftar) if m.nim == nim
    ), None )

    return {
        "message": "Berhasil masuk antrian", 
        "posisi": posisi,
        "antrian_id": antrian.id_antrian
    }