from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.models.layanan import *
from app.schemas.layanan import *
from app.utils.supabase_client import *
# from app.routes.websocket import manager 

from mimetypes import guess_type
from datetime import datetime
from uuid import UUID

import asyncio
import uuid
import os

def create_layanan(db: Session, layanan: LayananSchema):
    db_layanan = Layanan(
        layanan_id = layanan.layanan_id,
        layanan_file = layanan.layanan_file,
        layanan_jenis = layanan.layanan_jenis,
        layanan_status = layanan.layanan_status
    )
    db.add(db_layanan)
    db.commit()
    db.refresh(db_layanan)
    return db_layanan

def get_layanan(db: Session, layanan_id: str):
    return db.query(Layanan).filter(Layanan.layanan_id == layanan_id).first()

def get_all_layanan(db: Session):
    return db.query(Layanan).order_by(Layanan.layanan_id.asc()).all()


# ============================
# JENIS LAYANAN
# ============================


def create_jenis_layanan(db: Session, data: JenisLayananCreate):
    jenis = JenisLayanan(**data.model_dump())
    db.add(jenis)
    db.commit()
    db.refresh(jenis)
    return jenis

def get_all_jenis_layanan(db: Session):
    return db.query(JenisLayanan).order_by(JenisLayanan.id).all()

def get_jenis_layanan_by_id(db: Session, id: int):
    return db.query(JenisLayanan).filter(JenisLayanan.id == id).first()

def update_jenis_layanan(db: Session, id: int, data: JenisLayananCreate):
    jenis = get_jenis_layanan_by_id(db, id)
    if not jenis:
        return None
    for key, value in data.model_dump().items():
        setattr(jenis, key, value)
    db.commit()
    db.refresh(jenis)
    return jenis

def delete_jenis_layanan(db: Session, id: int):
    jenis = get_jenis_layanan_by_id(db, id)
    if not jenis:
        return None
    db.delete(jenis)
    db.commit()
    return jenis


# ============================
# DOKUMEN PERSYARATAN
# ============================


def create_dokumen(db: Session, data: DokumenPersyaratanCreate):
    dok = DokumenPersyaratan(**data.model_dump())
    db.add(dok)
    db.commit()
    db.refresh(dok)
    return dok

def get_dokumen_by_jenis_layanan(db: Session, jenis_id: int):
    return db.query(DokumenPersyaratan).filter(DokumenPersyaratan.jenis_layanan_id == jenis_id).all()

def delete_dokumen(db: Session, id: int):
    dok = db.query(DokumenPersyaratan).filter(DokumenPersyaratan.id == id).first()
    if dok:
        db.delete(dok)
        db.commit()
    return dok


# ============================
# PENGAJUAN LAYANAN
# ============================


def create_pengajuan(db: Session, data: PengajuanLayananCreate):
    pengajuan = PengajuanLayanan(**data.model_dump())
    db.add(pengajuan)
    db.commit()
    db.refresh(pengajuan)
    return pengajuan

def get_all_pengajuan(db: Session):
    return db.query(PengajuanLayanan).order_by(PengajuanLayanan.created_at).all()

def get_pengajuan_by_mahasiswa(db: Session, nim: str):
    return db.query(PengajuanLayanan).filter(PengajuanLayanan.mahasiswa_nim == nim).all()

def update_status_pengajuan(db: Session, id: UUID, data: PengajuanUpdateSchema):
    pengajuan = db.query(PengajuanLayanan).filter(PengajuanLayanan.id == id).first()
    
    if pengajuan:
        pengajuan.status = data.status
        pengajuan.catatan_admin = data.catatan_admin
        pengajuan.jadwal_pengambilan = data.jadwal_pengambilan
        db.commit()
        db.refresh(pengajuan)

        # asyncio.get_event_loop().create_task(manager.send_personal_message({
        #     "id": str(pengajuan.id),
        #     "status": pengajuan.status,
        #     "mahasiswa_nim": pengajuan.mahasiswa_nim,
        #     "catatan_admin": pengajuan.catatan_admin,
        #     "jadwal_pengambilan": pengajuan.jadwal_pengambilan.isoformat() if pengajuan.jadwal_pengambilan else None
        # }, client_id=str(pengajuan.mahasiswa_nim)))

    return pengajuan


# ============================
# LAMPIRAN PENGAJUAN
# ============================


def create_lampiran(db: Session, data: LampiranPengajuanCreate):
    lampiran = LampiranPengajuan(**data.model_dump())
    db.add(lampiran)
    db.commit()
    db.refresh(lampiran)
    return lampiran

def get_lampiran_by_pengajuan(db: Session, pengajuan_id: UUID):
    return db.query(LampiranPengajuan).filter(LampiranPengajuan.pengajuan_id == pengajuan_id).all()


# ============================
# UPLOAD LAMPIRAN 
# ============================

def upload_to_supabase(file: UploadFile) -> str:
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    content_type = guess_type(file.filename)[0] or "application/octet-stream"

    file_bytes = file.file.read()
    
    supabase.storage.from_(BUCKET_NAME).upload(
        path = unique_filename,
        file = file_bytes,
        file_options={
            "content-type": content_type,
            "cache-control": "3600"
        }
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    return public_url

def save_uploaded_file_metadata(db, nama_dokumen, file_url, pengajuan_id):
    lampiran = LampiranPengajuan(
        pengajuan_id = pengajuan_id,
        nama_dokumen = nama_dokumen,
        file_url = file_url,
        uploaded_at = datetime.now()
    )
    db.add(lampiran)
    db.commit()
    db.refresh(lampiran)
    return lampiran