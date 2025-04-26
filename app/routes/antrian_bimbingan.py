from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.antrian_service import *
from app.schemas.antrian_bimbingan import *
from app.utils.dependencies import require_roles
from app.config import get_db

router = APIRouter(
    prefix="/antrian", 
    tags=["Antrian Bimbingan"],
    dependencies=[Depends(require_roles("mahasiswa"))])

@router.post("/", response_model=AmbilAntrianResponse)
async def ambil_antrian(data: AmbilAntrianSchema, db: Session = Depends(get_db)):
    return await ambil_antrian_bimbingan(db, data)

@router.get("/{id_antrian}", response_model=AntrianBimbinganSchema)
def get_antrian_route(id_antrian: int, db: Session = Depends(get_db)):
    return get_antrian_by_id(db, id_antrian)

@router.put("/f/{id_antrian}")
async def update_status_route(id_antrian: int, db: Session = Depends(get_db)):
    return await update_status_antrian(db, id_antrian)

@router.delete("/{id_antrian}")
def delete_antrian_route(id_antrian: int, db: Session = Depends(get_db)):
    return delete_antrian(id_antrian, db)