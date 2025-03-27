from sqlalchemy.orm import Session
from app.models.dosen import Dosen
from app.schemas.dosen import DosenSchema, DosenUpdateSchema
from app.utils.security import hash_password

def create_dosen(db: Session, dosen: DosenSchema):
    hashed_password = hash_password(dosen.password)
    db_dosen = Dosen(
        nomor_induk = dosen.nomor_induk,
        name = dosen.name,
        email = dosen.email,
        password = hashed_password,
        status_kehadiran = dosen.status_kehadiran,
        ketersediaan_bimbingan = dosen.ketersediaan_bimbingan,
        jumlah_bimbingan = dosen.jumlah_bimbingan,
    )
    db.add(db_dosen)
    db.commit()
    db.refresh(db_dosen)
    return db_dosen

def update_dosen(db: Session, nomor_induk: str, dosen_data: DosenUpdateSchema):
    dosen = db.query(Dosen).filter(Dosen.nomor_induk == nomor_induk).first()
    
    if not dosen:
        return None
    
    update_data = dosen_data.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(dosen, key, value)

    db.commit()
    db.refresh(dosen)
    return dosen

def get_dosen(db: Session, nomor_induk: str):
    return db.query(Dosen).filter(Dosen.nomor_induk == nomor_induk).first()

def get_all_dosen(db: Session):
    return db.query(Dosen).order_by(Dosen.nomor_induk.asc()).all()