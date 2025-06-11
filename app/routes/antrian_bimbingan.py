from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.services.antrian_service import *
from app.schemas.antrian_bimbingan import *
from app.middleware.security import get_current_mahasiswa
from app.database.session import get_db
from app.database.models.mahasiswa import Mahasiswa 

router = APIRouter(
    prefix="/antrian", 
    tags=["Antrian Bimbingan"]
    # dependencies=[Depends(require_roles("mahasiswa"))]
    )

@router.post("/", response_model=AmbilAntrianResponse)
async def ambil_antrian(waktu_id: str, mahasiswa_nim: str, file: UploadFile = File(None), db: Session = Depends(get_db)):
    return await ambil_antrian_bimbingan(db, waktu_id, mahasiswa_nim, file)

@router.get("/all", response_model=list[AntrianBimbinganSchema])
def get_all_antrian_route(db: Session = Depends(get_db)):
    antrian = db.query(AntrianBimbingan).all()
    return antrian

@router.get("/all/mahasiswa", response_model=list[AntrianBimbinganSchema])
def get_all_antrian_by_mahasiswa_route(db: Session = Depends(get_db), current_user: Mahasiswa = Depends(get_current_mahasiswa)):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.mahasiswa_nim == current_user.nim).all()
    if not antrian:
        raise HTTPException(status_code=404, detail="Tidak ada antrian ditemukan untuk mahasiswa ini.")
    return antrian

@router.get("/all/mahasiswa/{nim}", response_model=list[AntrianBimbinganSchema])
def get_all_antrian_by_nim_route(nim: str, db: Session = Depends(get_db)):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.mahasiswa_nim == nim).all()
    if not antrian:
        raise HTTPException(status_code=404, detail="Tidak ada antrian ditemukan untuk NIM ini.")
    return antrian

@router.get("/all/dosen/{inisial}", response_model=list[AntrianBimbinganSchema])
def get_all_antrian_by_dosen_route(inisial: str, db: Session = Depends(get_db)):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.dosen_inisial == inisial).all()
    if not antrian:
        raise HTTPException(status_code=404, detail="Tidak ada antrian ditemukan untuk dosen ini.")
    return antrian

@router.get("/{id_antrian}", response_model=AntrianBimbinganSchema)
def get_antrian_route(id_antrian: UUID, db: Session = Depends(get_db)):
    return get_antrian_by_id(db, id_antrian)

@router.patch("/{id_antrian}")
async def update_antrian_route(id_antrian: UUID, file: UploadFile = File(None), db: Session = Depends(get_db), current_user: Mahasiswa = Depends(get_current_mahasiswa)):
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == id_antrian).first()
    
    if not antrian:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan.")
    if antrian.mahasiswa_nim != current_user.nim:
        raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk memperbarui antrian ini.")   

    return await update_antrian(db, id_antrian, file)

@router.delete("/{id_antrian}")
async def delete_antrian_route(id_antrian: UUID, db: Session = Depends(get_db), current_user: Mahasiswa = Depends(get_current_mahasiswa)): 
    antrian = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == id_antrian).first()
    
    if not antrian:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan.")
    if antrian.mahasiswa_nim != current_user.nim:
        raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk menghapus antrian ini.")
    
    return await delete_antrian(id_antrian, db)

@router.patch("/f/{id_antrian}")
async def update_status_route(id_antrian: UUID, db: Session = Depends(get_db)):
    return await update_status_antrian(db, id_antrian)