from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.bimbingan_service import create_waktuBimbingan, get_waktuBimbingan, get_waktuBimbingan_from_dosen, get_waktuBimbingan_from_mahasiswa
from app.schemas.waktu_bimbingan import WaktuBimbinganSchema

from app.config import get_db

router = APIRouter(prefix="/waktu_bimbingan", tags=["Waktu Bimbingan"])

@router.post("/", response_model=WaktuBimbinganSchema)
def create_waktu_bimbingan_route(waktuBimbingan: WaktuBimbinganSchema, db: Session = Depends(get_db)):
    return create_waktuBimbingan(db, waktuBimbingan)

@router.get("/{id}", response_model=WaktuBimbinganSchema)
def get_waktu_bimbingan_route(idWaktu: int, db: Session = Depends(get_db)):
    return get_waktuBimbingan(db, idWaktu)

@router.get("/dosen/{nomor_induk}", response_model=list[WaktuBimbinganSchema])
def get_bimbingan_by_dosen(nomor_induk: str, db: Session = Depends(get_db)):
    return get_waktuBimbingan_from_dosen(db, nomor_induk)

@router.get("/mahasiswa/{nim}", response_model=list[WaktuBimbinganSchema])
def get_bimbingan_by_mahasiswa(nim: str, db: Session = Depends(get_db)):
    return get_waktuBimbingan_from_mahasiswa(db, nim)
