from sqlalchemy.orm import Session
from app.models.layanan import Layanan
from app.schemas.layanan import LayananSchema

def create_layanan(db: Session, layanan: LayananSchema):
    db_layanan = Layanan(
        layanan_id = layanan.layanan_id,
        layanan_file = layanan.layanan_file,
        layanan_jenis = layanan.layanan_jenis,
        layanan_status = layanan.layanan_status
    )
    db.add(db_layanan)
    db.commit()
    db.refresh(db_layanan)
    return db_layanan

def get_layanan(db: Session, layanan_id: str):
    return db.query(Layanan).filter(Layanan.layanan_id == layanan_id).first()

def get_all_layanan(db: Session):
    return db.query(Layanan).order_by(Layanan.layanan_id.asc()).all()