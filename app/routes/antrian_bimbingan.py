from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services.antrian_service import *
from app.schemas.antrian_bimbingan import *

from app.config import get_db

router = APIRouter(prefix="/antrian", tags=["Antrian Bimbingan"])

@router.post("/", response_model=AmbilAntrianResponse)
def ambil_antrian(data: AmbilAntrianSchema, db: Session = Depends(get_db)):
    return ambil_antrian_bimbingan(db, data)

@router.get("/{id_antrian}", response_model=AntrianBimbinganSchema)
def get_antrian_route(id_antrian: int, db: Session = Depends(get_db)):
    return get_antrian_by_id(db, id_antrian)
