from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.config import SessionLocal

from app.services.layanan import create_layanan, get_layanan, get_all_layanan
from app.schemas.layanan import LayananSchema 

router = APIRouter(prefix="/layanan", tags=["Layanan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LayananSchema)
def create_layanan_route(layanan: LayananSchema, db: Session = Depends(get_db)):
    return create_layanan(db, layanan)

@router.get("/all", response_model=list[LayananSchema])
def get_all_layanan_route(db: Session = Depends(get_db)):
    return get_all_layanan(db)

@router.get("/{layanan_id}", response_model=LayananSchema)
def get_layanan_route(layanan_id: int, db: Session = Depends(get_db)):
    layanan = get_layanan(db, layanan_id)
    if not layanan:
        raise HTTPException(status_code=404, detail="Layanan Tidak Ditemukan")
    return layanan
