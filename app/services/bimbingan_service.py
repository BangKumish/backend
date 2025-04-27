from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.waktu_bimbingan import WaktuBimbingan
from app.schemas.waktu_bimbingan import *

def create_waktu_bimbingan(db: Session, waktu_bimbingan_schema: CreateWaktuBimbinganSchema):
    
    db_waktu_bimbingan = WaktuBimbingan(
        dosen_inisial=waktu_bimbingan_schema.dosen_inisial,
        jumlah_antrian=waktu_bimbingan_schema.jumlah_antrian,
        tanggal=waktu_bimbingan_schema.tanggal,
        waktu_mulai=waktu_bimbingan_schema.waktu_mulai,
        waktu_selesai=waktu_bimbingan_schema.waktu_selesai,
        lokasi=waktu_bimbingan_schema.lokasi,
        keterangan=waktu_bimbingan_schema.keterangan
    )
    
    existing_count = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == waktu_bimbingan_schema.dosen_inisial).count()
    db_waktu_bimbingan.bimbingan_id = f"{waktu_bimbingan_schema.dosen_inisial.upper()}{existing_count + 1}"
    
    db.add(db_waktu_bimbingan)
    db.commit()
    db.refresh(db_waktu_bimbingan)
    return db_waktu_bimbingan

def get_waktu_bimbingan(db: Session, bimbingan_id: str):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not waktu:
        raise HTTPException(status_code=404, detail="Waktu bimbingan tidak ditemukan")
    return WaktuBimbinganSchema.model_validate(waktu)


def get_waktu_bimbingan_from_dosen(db: Session, dosen_inisial: str):
    waktu_list = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == dosen_inisial).order_by(WaktuBimbingan.bimbingan_id.asc()).all()
    return [WaktuBimbinganSchema.model_validate(waktu) for waktu in waktu_list]


def update_waktu_bimbingan(db: Session, bimbingan_id: str, _data: UpdateWaktuBimbinganSchema):
    record = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Waktu bimbingan tidak ditemukan")
    
    update_data = _data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_waktu_bimbingan(db: Session, bimbingan_id: str):
    _data = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    db.delete(_data)
    db.commit()

    return {
        "message": f"Jadwal Bimbingan telah dihapus"
    }

def generate_bimbingan_id(db: Session, dosen_inisial: str) -> str:
    count = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == dosen_inisial).count()
    new_id = f"{dosen_inisial}{count+1}"
    return new_id

# def create_waktuBimbingan(db: Session, waktuBimbinganSchema: CreateWaktuBimbinganScheme):
#     db_waktuBimbingan = WaktuBimbingan(
#         nomor_induk = waktuBimbinganSchema.nomor_induk,
#         jumlah_antrian = waktuBimbinganSchema.jumlah_antrian,
#         tanggal = waktuBimbinganSchema.tanggal,
#         waktu_mulai = waktuBimbinganSchema.waktu_mulai,
#         waktu_selesai = waktuBimbinganSchema.waktu_selesai
#     )
#     db.add(db_waktuBimbingan)
#     db.commit()
#     db.refresh(db_waktuBimbingan)
#     return db_waktuBimbingan

# def get_waktuBimbingan(db: Session, idWaktu: int):
#     waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()
#     if not waktu:
#         raise HTTPException(status_code=404, detail="Waktu bimbingan tidak ditemukan")

#     return WaktuBimbinganSchema.model_validate(waktu)

# def get_waktuBimbingan_from_dosen(db: Session, nomor_induk: str):
#     return db.query(WaktuBimbingan).filter(WaktuBimbingan.nomor_induk == nomor_induk).all()

# def get_waktuBimbingan_from_mahasiswa(db: Session, nim: str):
#     return db.query(WaktuBimbingan).filter(WaktuBimbingan.nim == nim).all()

# def update_waktuBimbingan(db: Session, idWaktu: int, _data: UpdateWaktuBimbinganScheme):
#     record = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()
    
#     if not _data:
#         return None
    
#     update_data = _data.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(record, key, value)

#     db.commit()
#     db.refresh(record)
#     return record

# def delete_waktuBimbingan(db: Session, idWaktu: int):
#     _data = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == idWaktu).first()
#     if not _data:
#         raise HTTPException(
#             status_code=404,
#             detail="Data tidak ditemukan"
#         )

#     # name = dosen_data.name
#     db.delete(_data)
#     db.commit()

#     return {
#         "message": f"Jadwal Bimbingan telah dihapus"
#     }