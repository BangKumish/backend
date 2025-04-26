from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.models.antrian_bimbingan import AntrianBimbingan
from app.models.waktu_bimbingan import WaktuBimbingan

from app.schemas.antrian_bimbingan import *

from app.routes.file import upload_file
from app.routes.websocket import manager

from datetime import datetime
from uuid import uuid4

def get_antrian_by_id(db: Session, id_antrian: UUID):
    return db.query(AntrianBimbingan)\
        .options(joinedload(AntrianBimbingan.files))\
        .filter(AntrianBimbingan.id_antrian == id_antrian)\
        .first()

async def ambil_antrian_bimbingan(db: Session, waktu_id: int, nim: str, file: Optional[UploadFile] = None):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == waktu_id).first()
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
    
    daftar = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).order_by(AntrianBimbingan.created_at).all()
    posisi = jumlah + 1
    
    # posisi = next((
    #     i+1 for i, m in enumerate(daftar) if m.nim == mahasiswa_nim
    # ), None )
    
    antrianId = uuid4()
    antrian = AntrianBimbingan(
        id_antrian = antrianId,
        mahasiswa_nim = nim,
        waktu_id = waktu_id,
        dosen_inisial = waktu.nomor_induk,
        status_antrian = "Menunggu",
        position = posisi,
        created_at = datetime.now()
    )
    db.add(antrian)
    db.commit()
    db.refresh(antrian)

    uploaded_file = None
    if file:
        uploaded_file = await upload_file(
            antrian_id = antrianId,
            mahasiswa_nim = nim,
            file = file,
            db = db
        )

    await manager.broadcast_to_room(f"bimbingan_{dosen.alias}", {
        "event": "update_antrian",
        "inisial": dosen.alias,
        "waktu_id": waktu.id,
        "tanggal": str(waktu.tanggal),
        "queue": [
            {
                "id_antrian": item.id_antrian,
                "nim": item.mahasiswa_nim,
                "status": item.status_antrian
            } for item in daftar
        ]
    })

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

async def update_status_antrian(db: Session, id_antrian: UUID):
    antrian = db.query(AntrianBimbingan).filter_by(id_antrian=id_antrian).first()

    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak Ditemukan."
        )

    # 1. Tandai antrian ini sebagai "Selesai"
    antrian.status_antrian = "Selesai"
    db.commit()
    db.refresh(antrian)

    # 2. Cari Waktu Bimbingannya
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == antrian.waktu_id).first()

    # 3. Cari dan update antrian selanjutnya
    if waktu:
        next_position = antrian.position + 1  # cari posisi berikutnya

        next_antrian = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.id,
            position=next_position,
            status_antrian="Menunggu"  # pastikan statusnya masih Menunggu
        ).first()

        if next_antrian:
            next_antrian.status_antrian = "Dalam Bimbingan"
            db.commit()
            db.refresh(next_antrian)

        # 4. Ambil semua daftar antrian terbaru untuk broadcast
        daftar = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.id
        ).order_by(AntrianBimbingan.position).all()

        await manager.broadcast_to_room(f"bimbingan_{antrian.dosen_inisial}", {
            "event": "update_antrian",
            "inisial": antrian.dosen_inisial,
            "waktu_id": waktu.id,
            "tanggal": str(waktu.tanggal),
            "queue": [
                {
                    "id_antrian": item.id_antrian,
                    "nim": item.mahasiswa_nim,
                    "status": item.status_antrian
                } for item in daftar
            ]
        })

    return {"message": "Status antrian diperbaharui menjadi Selesai dan antrian berikutnya mulai Dalam Bimbingan."}


# async def update_status_antrian(db: Session, id_antrian: UUID):
#     antrian = db.query(AntrianBimbingan).filter_by(id_antrian=id_antrian).first()

#     if not antrian:
#         raise HTTPException(
#             status_code=404,
#             detail="Antrian tidak Ditemukan."
#         )
    
#     antrian.status_antrian = "Selesai"
#     db.commit()
#     db.refresh(antrian)

#     waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == antrian.waktu_id).first()
#     if waktu:
#         daftar = db.query(AntrianBimbingan).filter_by(
#             waktu_id=waktu.id
#         ).order_by(AntrianBimbingan.waktu_antrian).all()

#         await manager.broadcast_to_room(f"bimbingan_{antrian.dosen_inisial}", {
#             "event": "update_antrian",
#             "inisial": antrian.dosen_inisial,
#             "waktu_id": waktu.id,
#             "tanggal": str(waktu.tanggal),
#             "queue": [
#                 {
#                     "id_antrian": item.id_antrian,
#                     "nim": item.mahasiswa_nim,
#                     "status": item.status_antrian
#                 } for item in daftar
#             ]
#         })

#     return {"message": f"Status antrian diperbaharui menjadi Selesai."}

def delete_antrian(idAntrian: UUID, db: Session):
    _data = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == idAntrian).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    # name = dosen_data.name
    db.delete(_data)
    db.commit()

    return {
        "message": f"Antrian telah dihapus"
    }