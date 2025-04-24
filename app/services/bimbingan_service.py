from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.waktu_bimbingan import WaktuBimbingan
from app.schemas.waktu_bimbingan import CreateWaktuBimbinganScheme, WaktuBimbinganSchema, UpdateWaktuBimbinganScheme

def create_waktuBimbingan(db: Session, waktuBimbinganSchema: CreateWaktuBimbinganScheme):
    db_waktuBimbingan = WaktuBimbingan(
        nomor_induk = waktuBimbinganSchema.nomor_induk,
        jumlah_antrian = waktuBimbinganSchema.jumlah_antrian,
        tanggal = waktuBimbinganSchema.tanggal,
        waktu_mulai = waktuBimbinganSchema.waktu_mulai,
        waktu_selesai = waktuBimbinganSchema.waktu_selesai
    )
    db.add(db_waktuBimbingan)
    db.commit()
    db.refresh(db_waktuBimbingan)
    return db_waktuBimbingan

def get_waktuBimbingan(db: Session, idWaktu: int):
    return db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()

def get_waktuBimbingan_from_dosen(db: Session, nomor_induk: str):
    return db.query(WaktuBimbingan).filter(WaktuBimbingan.nomor_induk == nomor_induk).all()

def get_waktuBimbingan_from_mahasiswa(db: Session, nim: str):
    return db.query(WaktuBimbingan).filter(WaktuBimbingan.nim == nim).all()

def update_waktuBimbingan(db: Session, idWaktu: int, _data: UpdateWaktuBimbinganScheme):
    record = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()
    
    if not _data:
        return None
    
    update_data = _data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

def delete_waktuBimbingan(db: Session, idWaktu: int):
    _data = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    # name = dosen_data.name
    db.delete(_data)
    db.commit()

    return {
        "message": f"Jadwal Bimbingan telah dihapus"
    }