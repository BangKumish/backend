from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.config import SessionLocal

from app.services.mahasiswa import create_mahasiswa
from app.services.mahasiswa import get_all_mahasiswa
from app.services.mahasiswa import get_mahasiswa

from app.services.waktu_bimbingan import get_waktuBimbingan_from_mahasiswa

from app.schemas.mahasiswa import MahasiswaSchema


router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MahasiswaSchema)
def create_mahasiswa_route(mahasiswa: MahasiswaSchema, db: Session = Depends(get_db)):
    return create_mahasiswa(db, mahasiswa)

@router.get("/all", response_model=list[MahasiswaSchema])
def get_all_mahasiswa_route(db: Session = Depends(get_db)):
    return get_all_mahasiswa(db)

@router.get("/{nim}", response_model=MahasiswaSchema)
def get_mahasiswa_route(nim: str, db: Session = Depends(get_db)):
    data = get_mahasiswa(db, nim)
    if not data:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    waktu_bimbingan = get_waktuBimbingan_from_mahasiswa(db, nim)
    
    return JSONResponse (content={
        "dosen": {
            "id": data.nim,
            "nama": data.nama,
            "email": data.email
        },
        "waktu_bimbingan": [
            {
                "id": item.id,
                "tanggal": str(item.tanggal),
                "waktu_mulai": str(item.waktu_mulai),
                "waktu_selesai": str(item.waktu_selesai)
            }
            for item in waktu_bimbingan
        ]
    })


