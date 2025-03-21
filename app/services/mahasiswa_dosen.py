from sqlalchemy.orm import Session
from app.models.mahasiswa_dosen import MahasiswaDosen
from app.schemas.mahasiswa_dosen import MahasiswaDosenSchema
from fastapi import HTTPException

def assign_dosen(db: Session, assigment: MahasiswaDosenSchema):
    existing_roles = db.query(MahasiswaDosen).filter(
        MahasiswaDosen.mahasiswa_nim == assigment.mahasiswa_nim,
        MahasiswaDosen.role == assigment.role
    ).count()

    if "Dosen Pembimbing" in assigment.role and existing_roles >= 2:
        raise HTTPException(status_code=400, detail="Maksimal 2 Dosen Pembimbing")
    
    if "Dosen Penguji" in assigment.role and existing_roles >= 2:
        raise HTTPException(status_code=400, detail="Maksimal 2 Dosen Penguji")
    
    new_assigment = MahasiswaDosen(**assigment.model_dump())
    db.add(new_assigment)
    db.commit()
    db.refresh(new_assigment)
    return new_assigment