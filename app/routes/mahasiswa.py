from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from uuid import UUID

from app.services.mahasiswa import *
from app.schemas.mahasiswa import *

from app.config import get_db

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

@router.post("/", response_model=MahasiswaCreateSchema)
def create_mahasiswa_route(mahasiswa: MahasiswaResponseSchema, db: Session = Depends(get_db)):
    return create_mahasiswa(db, mahasiswa)

@router.get("/all", response_model=list[MahasiswaCreateSchema])
def get_all_mahasiswa_route(db: Session = Depends(get_db)):
    return get_all_mahasiswa(db)

@router.get("/{nim}", response_model=MahasiswaCreateSchema)
def get_mahasiswa_route(nim: str, db: Session = Depends(get_db)):
    return get_mahasiswa(db, nim)

@router.get("/admin/{id}", response_model=MahasiswaSchema)
def get_detail_mahasiswa_route(id: UUID, db: Session = Depends(get_db)):
    return get_detail_mahasiswa(db, id)

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