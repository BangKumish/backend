from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.bimbingan_service import *
from app.schemas.waktu_bimbingan import *

from app.config import get_db

router = APIRouter(prefix="/waktu_bimbingan", tags=["Waktu Bimbingan"])

@router.post("/", response_model=WaktuBimbinganSchema)
def create_waktu_bimbingan_route(waktuBimbingan: CreateWaktuBimbinganScheme, db: Session = Depends(get_db)):
    return create_waktuBimbingan(db, waktuBimbingan)

@router.get("/{id}", response_model=WaktuBimbinganSchema)
def get_waktu_bimbingan_route(idWaktu: int, db: Session = Depends(get_db)):
    return get_waktuBimbingan(db, idWaktu)

@router.get("/dosen/{nomor_induk}", response_model=list[WaktuBimbinganSchema])
def get_bimbingan_by_dosen(nomor_induk: str, db: Session = Depends(get_db)):
    return get_waktuBimbingan_from_dosen(db, nomor_induk)

@router.put("/dosen/{idWaktu}", response_model=WaktuBimbinganSchema)
def update_waktu_bimbingan_route(idWaktu: int, updated_data: UpdateWaktuBimbinganScheme, db: Session = Depends(get_db)):
    return update_waktuBimbingan(db, idWaktu, updated_data)

@router.delete("/dosen/{idWaktu}")
def delete_waktu_bimbingan_route(idWaktu: int, db: Session = Depends(get_db)):
    return delete_waktuBimbingan(db, idWaktu)
