from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.schemas.mahasiswa import *

from app.database.models.mahasiswa import Mahasiswa
from app.database.models.user import User

from app.database.models.mahasiswa_dosen import MahasiswaDosen

from app.middleware.jwt_handler import hash_password
import uuid

def create_mahasiswa(db: Session, mahasiswa: MahasiswaSchema):
    hashed_password = hash_password(mahasiswa.password) 
    mahasiswa_id = uuid.uuid4()
    
    db_mahasiswa = Mahasiswa(
        id=mahasiswa_id,
        nim=mahasiswa.nim,
        nama=mahasiswa.nama,
        email=mahasiswa.email,
        password=hashed_password,
    )
    db.add(db_mahasiswa)
    db.commit()
    db.refresh(db_mahasiswa)

    db_user = User(
        user_id = mahasiswa_id,
        email = mahasiswa.email,
        password = hashed_password,
        role = "mahasiswa"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_mahasiswa

def get_mahasiswa(db: Session, nim: str):
    return db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()

def get_all_mahasiswa(db: Session):
    return db.query(Mahasiswa).order_by(Mahasiswa.nim.asc()).all()

def get_detail_mahasiswa(db: Session, id: UUID):
    return db.query(Mahasiswa).filter(Mahasiswa.id == id).first()

def get_mahasiswa_detail(db: Session, nim:str):
    return (
        db.query(Mahasiswa)
        .options(
            joinedload(Mahasiswa.dosen_relation).joinedload(MahasiswaDosen.dosen)
        )
        .filter(Mahasiswa.nim == nim)
        .first()
    )

def update_mahasiswa(db: Session, nim: str, mahasiswa_data: MahasiswaUpdateSchema):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    
    if not mahasiswa:
        return None
    
    update_data = mahasiswa_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(mahasiswa, key, value)

    db.commit()
    db.refresh(mahasiswa)
    return mahasiswa

def delete_mahasiswa(db: Session, mahasiswa_id: UUID):
    _data = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data Mahasiswa Tidak Ditemukan"
        )

    name = _data.nama
    user_data = db.query(User).filter(User.user_id == mahasiswa_id).first
    if user_data:
        db.delete(user_data)

    db.delete(_data)
    db.commit()

    return {
        "message": f"Data Mahasiswa {name} telah dihapus"
    }