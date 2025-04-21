from sqlalchemy.orm import Session
from app.models.waktu_bimbingan import WaktuBimbingan
from app.schemas.waktu_bimbingan import WaktuBimbinganSchema

def create_waktuBimbingan(db: Session, waktuBimbinganSchema: WaktuBimbinganSchema):
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
