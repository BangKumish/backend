from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.database.models.antrian_bimbingan import AntrianBimbingan
from app.database.models.waktu_bimbingan import WaktuBimbingan

from app.schemas.antrian_bimbingan import *

from app.routes.file import upload_file
from app.routes.websocket_router import manager

from datetime import datetime
from uuid import uuid4

import asyncio

def get_antrian_by_id(db: Session, id_antrian: UUID):
    return db.query(AntrianBimbingan)\
        .options(joinedload(AntrianBimbingan.files))\
        .filter(AntrianBimbingan.id_antrian == id_antrian)\
        .first()

async def ambil_antrian_bimbingan(db: Session, waktu_id: str, nim: str, file: Optional[UploadFile] = None):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == waktu_id).first()
    if not waktu:
        raise HTTPException(
            status_code=404,
            detail="Waktu bimbingan tidak ditemukan."
        )
    
    dosen = waktu.dosen
    
    sudah_ada = db.query(AntrianBimbingan).filter_by(mahasiswa_nim=nim, waktu_id=waktu_id).first()
    if sudah_ada:
        raise HTTPException(
            status_code=400,
            detail="Anda sudah masuk antrian."
        )
    
    jumlah = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).count()
    if jumlah >= waktu.jumlah_antrian:
        raise HTTPException(
            status_code=400,
            detail="Slot penuh."
        )
    
    posisi = jumlah + 1
    
    antrianId = uuid4()
    antrian = AntrianBimbingan(
        id_antrian = antrianId,
        mahasiswa_nim = nim,
        waktu_id = waktu_id,
        dosen_inisial = waktu.dosen_inisial,
        status_antrian = "Menunggu",
        position = posisi,
        created_at = datetime.now()
    )
    db.add(antrian)
    db.commit()
    db.refresh(antrian)

    daftar = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).order_by(AntrianBimbingan.created_at).all()

    uploaded_file = None
    if file:
        uploaded_file = await upload_file(
            antrian_id = antrianId,
            mahasiswa_nim = nim,
            file = file,
            db = db
        )

    queue_data = [
        {
            "id_antrian": str(item.id_antrian),
            "nim": item.mahasiswa_nim,
            "status": item.status_antrian
        }
        for item in daftar
    ]

    payload = {
        "event": "update_antrian",
        "inisial": dosen.alias,
        "waktu_id": waktu.bimbingan_id,
        "tanggal": str(waktu.tanggal),
        "queue": queue_data
    }

    send_tasks = [
    manager.send_json(user_id=item.mahasiswa_nim, data=payload)
    for item in daftar
    ]

    send_tasks.append(
        manager.send_json(user_id=dosen.alias, data=payload)
    )

    await asyncio.gather(*send_tasks)

    return AmbilAntrianResponse(
        message="Berhasil masuk antrian",
        posisi=posisi,
        id_antrian=antrian.id_antrian,
        antrian=AmbilAntrianSchema(
            mahasiswa_nim=antrian.mahasiswa_nim,
            waktu_id=antrian.waktu_id
    ),
    files=FileSchema.model_validate(uploaded_file) if uploaded_file else None
)

async def notify_position_change(nim: str, position: int):
    await manager.send_message(nim, f"Posisi Anda di antrian: {position}")

def delete_antrian_file(db: Session, id_antrian: UUID):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == id_antrian).first()
    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak ditemukan."
        )
    
    if antrian.files:
        db.delete(antrian.files)
        db.commit()
        db.refresh(antrian)

    return {
        "message": "File antrian berhasil dihapus."
    }

async def update_antrian(db: Session, id_antrian: UUID, file: Optional[UploadFile] = None):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == id_antrian).first()
    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak ditemukan."
        )
    
    try:
        if file:
            if antrian.files:
                db.delete(antrian.files)
                db.flush()

            uploaded_file = await upload_file(
                antrian_id = antrian.id_antrian,
                mahasiswa_nim = antrian.mahasiswa_nim,
                file = file,
                db = db
            )

            if uploaded_file:
                antrian.files = uploaded_file

        db.commit()
        db.refresh(antrian)

        return{
            "message": "File berhasil diperbarui.",
            "data": antrian
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan saat memperbarui antrian: {str(e)}"
        )

async def update_status_antrian(db: Session, id_antrian: UUID):
    antrian = db.query(AntrianBimbingan).filter_by(id_antrian=id_antrian).first()

    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak ditemukan."
        )

    original_status = antrian.status_antrian

    if antrian.status_antrian == "Menunggu":
        antrian.status_antrian = "Dalam Bimbingan"
    elif antrian.status_antrian == "Dalam Bimbingan":
        antrian.status_antrian = "Selesai"
    
    db.commit()
    db.refresh(antrian)

    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == antrian.waktu_id).first()

    if waktu:
        all_selesai = db.query(AntrianBimbingan).filter(
            AntrianBimbingan.waktu_id == antrian.waktu_id,
            AntrianBimbingan.status_antrian != "Dalam Bimbingan"
        ).count() == 0

        if all_selesai:
            waktu.is_active = False
            db.commit()
            db.refresh(waktu)

    if waktu:
        daftar = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.bimbingan_id
        ).order_by(AntrianBimbingan.position).all()

        payload = {
            "event": "update_antrian",
            "inisial": antrian.dosen_inisial,
            "waktu_id": waktu.bimbingan_id,
            "tanggal": str(waktu.tanggal),
            "queue": [
                {
                    "id_antrian": str(item.id_antrian),
                    "nim": item.mahasiswa_nim,
                    "status": item.status_antrian
                } for item in daftar
            ]
        }

        send_tasks = [
            manager.send_json(user_id=item.mahasiswa_nim, data=payload)
            for item in daftar
        ]

        # Kirim ke dosennya juga
        send_tasks.append(
            manager.send_json(user_id=antrian.dosen_inisial, data=payload)
        )

        await asyncio.gather(*send_tasks)

    return {"message": f"Status antrian diperbaharui menjadi {antrian.status_antrian}."}

async def delete_antrian(idAntrian: UUID, db: Session):
    _data = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == idAntrian).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    deleted_position = _data.position
    dosen_inisial = _data.dosen_inisial
    waktu_id = _data.waktu_id
    deleted_mahasiswa_nim = _data.mahasiswa_nim

    try:
        db.delete(_data)
        db.flush()

        antrian_to_update = db.query(AntrianBimbingan).filter(
            AntrianBimbingan.position > deleted_position,
            AntrianBimbingan.dosen_inisial == dosen_inisial,
            AntrianBimbingan.waktu_id == waktu_id
        ).all()

        for antrian in antrian_to_update:
            antrian.position -= 1

        db.commit()

        waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == waktu_id).first()
        if waktu:
            daftar = db.query(AntrianBimbingan).filter_by(
                waktu_id=waktu.bimbingan_id
            ).order_by(AntrianBimbingan.position).all()

            payload = {
                "event": "delete_antrian",
                "inisial": dosen_inisial,
                "waktu_id": waktu.bimbingan_id,
                "tanggal": str(waktu.tanggal),
                "deleted_antrian": {
                    "id_antrian": str(idAntrian),
                    "nim": deleted_mahasiswa_nim,
                    "position": deleted_position
                },
                "queue": [
                    {
                        "id_antrian": str(item.id_antrian),
                        "nim": item.mahasiswa_nim,
                        "status": item.status_antrian,
                        "position": item.position
                    } for item in daftar
                ]
            }

            send_tasks = []

            for item in daftar:
                send_tasks.append(
                    manager.send_json(user_id=item.mahasiswa_nim, data=payload) 
                )
            
            send_tasks.append(
                manager.send_json(user_id=dosen_inisial, data=payload)
            )

            deleted_payload = {
                "event": "antrian_deleted",
                "message": "Antrian Anda telah dihapus",
                "id_antrian": str(idAntrian)
            }

            send_tasks.append(
                manager.send_json(user_id=deleted_mahasiswa_nim, data=deleted_payload)
            )

            await asyncio.gather(*send_tasks, return_exceptions=True)

        return {
            "message": f"Antrian telah dihapus",
            "deleted_antrian": {
                "id_antrian": str(_data.id_antrian),
                "position": deleted_position,
                "mahasiswa_nim": _data.mahasiswa_nim,
            },
            "updated_positions": len(antrian_to_update)
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan saat menghapus antrian: {str(e)}"
        )