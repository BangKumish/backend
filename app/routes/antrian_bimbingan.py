from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services.antrian_service import *
from app.schemas.antrian_bimbingan import AntrianBimbinganSchema

router = APIRouter(prefix="/antrian", tags=["Antrian Bimbingan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AntrianBimbinganSchema)
def create_antrian_route(antrian: AntrianBimbinganSchema, db: Session = Depends(get_db)):
    return create_antrian(db, antrian)

@router.get("/{id_antrian}", response_model=AntrianBimbinganSchema)
def get_antrian_route(id_antrian: int, db: Session = Depends(get_db)):
    return get_antrian_by_id(db, id_antrian)

def ambil_antrian(waktu_id: int, nim: str, db: Session = Depends(get_db)):
    return ambil_antrian_bimbingan(db, nim, waktu_id)