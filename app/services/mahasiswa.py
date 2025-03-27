from sqlalchemy.orm import Session
from app.models.mahasiswa import Mahasiswa
from app.schemas.mahasiswa import MahasiswaSchema, MahasiswaUpdateSchema
from app.utils.security import hash_password

def create_mahasiswa(db: Session, mahasiswa: MahasiswaSchema):
    hashed_password = hash_password(mahasiswa.password) 

    db_mahasiswa = Mahasiswa(
        nim=mahasiswa.nim,
        nama=mahasiswa.nama,
        email=mahasiswa.email,
        password=hashed_password,
        topik_penelitian=mahasiswa.topik_penelitian
    )
    db.add(db_mahasiswa)
    db.commit()
    db.refresh(db_mahasiswa)
    return db_mahasiswa

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

def get_mahasiswa(db: Session, nim: str):
    return db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()

def get_all_mahasiswa(db: Session):
    return db.query(Mahasiswa).order_by(Mahasiswa.nim.asc()).all()