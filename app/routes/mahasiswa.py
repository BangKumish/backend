from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.config import SessionLocal

from app.services.mahasiswa import create_mahasiswa
from app.services.mahasiswa import get_all_mahasiswa
from app.services.mahasiswa import get_mahasiswa
from app.services.mahasiswa import update_mahasiswa

from app.services.waktu_bimbingan import get_waktuBimbingan_from_mahasiswa

from app.schemas.mahasiswa import MahasiswaSchema, MahasiswaUpdateSchema


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

@router.put("/{nim}")
def update_mahasiswa_route(nim: str, update_data: MahasiswaUpdateSchema, db: Session = Depends(get_db)):
    data = update_mahasiswa(db, nim, update_data)
    if not data:
        raise HTTPException(status_code = 404, detail = "Mahasiswa Tidak Ditemukan")
    return {"Message": "Mahasiswa Telah diUpdate", "data":data}

@router.get("/detail/{nim}")
def get_mahasiswa_detail(nim: str, db: Session = Depends(get_db)):
    mahasiswa = get_mahasiswa(db, nim)
    if not mahasiswa:
        raise HTTPException(
            status_code=404,
            detail="Mahasiswa not Found"
        )

    from app.routes.mahasiswa_dosen import get_all_relation_by_mahasiswa

    dosen_roles = {
        "Dosen Wali": None,
        "Dosen KP": None,
        "Dosen Pembimbing 1": None,
        "Dosen Pembimbing 2": None,
        "Dosen Penguji 1": None,
        "Dosen Penguji 2": None
    }

    for relasi in mahasiswa.dosen_relation:
        if relasi.dosen:
            role = relasi.role
            dosen_roles[role] = {
                "nama": relasi.dosen.name,
                "alias": relasi.dosen.alias
            }

    response = {
        "mahasiswa": {
            "nama": mahasiswa.nama,
            "nim": mahasiswa.nim,
            "email": mahasiswa.email,
            "tugas_akhir": {
                "judul": mahasiswa.topik_penelitian,
                "status": "Belum Ditentukan"
            }
        },
        "mahasiswa_dosen": dosen_roles
    }

    return JSONResponse(content=response)