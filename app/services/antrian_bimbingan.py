from sqlalchemy.orm import Session
from app.models.antrian_bimbingan import AntrianBimbingan
from app.schemas.antrian_bimbingan import AntrianBimbinganSchema

def create_antrian(db: Session, antrian: AntrianBimbinganSchema):
    db_antrian = AntrianBimbingan(**antrian.dict())
    db.add(db_antrian)
    db.commit()
    db.refresh(db_antrian)
    return db_antrian

def get_antrian_by_id(db: Session, id_antrian: int):
    return db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == id_antrian).first()
