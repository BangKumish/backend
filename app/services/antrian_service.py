from fastapi import HTTPException

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.models.antrian_bimbingan import AntrianBimbingan
from app.schemas.antrian_bimbingan import *

from app.models.waktu_bimbingan import WaktuBimbingan

from app.routes.websocket import manager

from datetime import datetime

def get_antrian_by_id(db: Session, id_antrian: int):
    return db.query(AntrianBimbingan)\
        .options(joinedload(AntrianBimbingan.files))\
        .filter(AntrianBimbingan.id_antrian == id_antrian)\
        .first()

async def ambil_antrian_bimbingan(db: Session, data: AmbilAntrianSchema):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == data.waktu_id).first()
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
    
    sudah_ada = db.query(AntrianBimbingan).filter_by(nim=data.nim, waktu_id=data.waktu_id).first()
    if sudah_ada:
        raise HTTPException(
            status_code=400,
            detail="Anda sudah masuk antrian."
        )
    
    jumlah = db.query(AntrianBimbingan).filter_by(waktu_id=data.waktu_id).count()
    if jumlah >= waktu.jumlah_antrian:
        raise HTTPException(
            status_code=400,
            detail="Slot penuh."
        )
    
    antrian = AntrianBimbingan(
        nim = data.nim,
        waktu_id = data.waktu_id,
        nomor_induk = waktu.nomor_induk,
        status_antrian = "Menunggu",
        waktu_antrian = datetime.now()
    )
    db.add(antrian)
    db.commit()
    db.refresh(antrian)

    daftar = db.query(AntrianBimbingan).filter_by(
        waktu_id=data.waktu_id
    ).order_by(AntrianBimbingan.waktu_antrian).all()
    
    posisi = next((
        i+1 for i, m in enumerate(daftar) if m.nim == data.nim
    ), None )

    await manager.broadcast_to_room(f"bimbingan_{dosen.alias}", {
        "event": "update_antrian",
        "inisial": dosen.alias,
        "waktu_id": waktu.id,
        "tanggal": str(waktu.tanggal),
        "queue": [
            {
                "id_antrian": item.id_antrian,
                "nim": item.nim,
                "status": item.status_antrian
            } for item in daftar
        ]
    })

    return {
        "message": "Berhasil masuk antrian", 
        "posisi": posisi,
        "antrian_id": antrian.id_antrian,
        "antrian":{
            "nim": data.nim,
            "waktu_id": data.waktu_id
        }
    }

async def notify_position_change(nim: str, position: int):
    await manager.send_message(nim, f"Posisi Anda di antrian: {position}")

async def update_status_antrian(db: Session, id_antrian: int):
    antrian = db.query(AntrianBimbingan).filter_by(id_antrian=id_antrian).first()

    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak Ditemukan."
        )
    
    antrian.status_antrian = "Selesai"
    db.commit()
    db.refresh(antrian)

    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.id == antrian.waktu_id).first()
    if waktu:
        daftar = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.id
        ).order_by(AntrianBimbingan.waktu_antrian).all()

        await manager.broadcast_to_room(f"bimbingan_{antrian.nomor_induk}", {
            "event": "update_antrian",
            "inisial": antrian.nomor_induk,
            "waktu_id": waktu.id,
            "tanggal": str(waktu.tanggal),
            "queue": [
                {
                    "id_antrian": item.id_antrian,
                    "nim": item.nim,
                    "status": item.status_antrian
                } for item in daftar
            ]
        })

    return {"message": f"Status antrian diperbaharui menjadi Selesai."}

def delete_antrian(idAntrian: int, db: Session):
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