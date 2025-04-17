from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.config import SessionLocal

from app.services.dosen import create_dosen, get_dosen, get_all_dosen, update_dosen
from app.services.waktu_bimbingan import get_waktuBimbingan_from_dosen

from app.schemas.dosen import DosenSchema, DosenUpdateSchema

from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/dosen", tags=["Dosen"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DosenSchema)
def create_dosen_route(dosen: DosenSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only Admin can Create Dosen") 
    return create_dosen(db, dosen)

@router.get("/all", response_model=list[DosenSchema])
def get_all_dosen_route(db: Session = Depends(get_db)):
    return get_all_dosen(db)

@router.get("/{nomor_induk}", response_model=DosenSchema)
def get_dosen_route(nomor_induk: str, db: Session = Depends(get_db)):
    
    data = get_dosen(db, nomor_induk)
    if not data:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    waktu_bimbingan = get_waktuBimbingan_from_dosen(db, nomor_induk)
    
    return JSONResponse (content={
        "dosen": {
            "id": data.nomor_induk,
            "name": data.name,
            "alias": data.alias,
            "email": data.email,
            "status_kehadiran": data.status_kehadiran,
            "ketersediaan_bimbingan": data.ketersediaan_bimbingan,
        },
        "waktu_bimbingan": [
            {
                "id": item.id,
                "tanggal": str(item.tanggal),
                "waktu_mulai": str(item.waktu_mulai),
                "waktu_selesai": str(item.waktu_selesai)
            }
            for item in waktu_bimbingan
        ]
    })

@router.put("/{nomor_induk}")
def update_dosen_route(nomor_induk: str, dosen_data: DosenUpdateSchema, db: Session = Depends(get_db)):
    dosen = update_dosen(db, nomor_induk, dosen_data)
    if not dosen:
        raise HTTPException(status_code = 404, detail = "Dosen Tidak Ditemukan")
    return {"Message": "Dosen Telah diUpdate", "data":dosen}
