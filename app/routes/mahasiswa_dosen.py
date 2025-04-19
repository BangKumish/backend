from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.schemas.mahasiswa_dosen import *
from app.services.mahasiswa_dosen import *

router = APIRouter(prefix="/relation", tags=["Mahasiswa-Dosen"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MahasiswaDosenSchema)
def create_relation(relation: MahasiswaDosenCreateSchema, db: Session = Depends(get_db)):
    return assign_dosen(db, relation)

@router.get("/", response_model=list[MahasiswaDosenSchema])
def get_all_relation(db: Session = Depends(get_db)):
    return get_relation(db)

@router.get("/mahasiswa/{nim}", response_model=list[MahasiswaDosenSchema])
def get_all_relation_by_mahasiswa(nim:str, db: Session = Depends(get_db)):
    return get_relation_by_mahasiswa(db, nim)

@router.get("/dosen/{alias}")
def get_all_relation_by_dosen(alias:str, db: Session = Depends(get_db)):
    relations = get_relation_by_dosen(db, alias)

    daftar_mahasiswa = []
    for relation in relations:
        if relation.mahasiswa:
            daftar_mahasiswa.append({
                "id": relation.id,
                "nama": relation.mahasiswa.nama,
                "nim": relation.mahasiswa.nim,
                "role": relation.role
            })
            
    return {
        "Daftar Mahasiswa": daftar_mahasiswa
        }

@router.put("/{id}", response_model=list[MahasiswaDosenSchema])
def edit_relation(
    id:int,
    update:MahasiswaDosenUpdateSchema,
    db: Session = Depends(get_db)
    ):
    relation = update_relation(db, id)

@router.delete("/{id}", response_model=MahasiswaDosenSchema)
def delete_relation(id:int, db: Session = Depends(get_db)):
    return delete_relation_by_id(db, id)