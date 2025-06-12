from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.dosen_service import *
from app.services.bimbingan_service import *

from app.schemas.dosen import *

from app.middleware.security import require_roles

router = APIRouter(prefix="/dosen", tags=["Dosen"])

@router.post("/", response_model=DosenResponseSchema, dependencies=[Depends(require_roles("admin"))])
def create_dosen_route(dosen: DosenCreateSchema, db: Session = Depends(get_db)):
    return create_dosen(db, dosen)

@router.get("/all", response_model=list[DosenResponseSchema])
def get_all_dosen_route(db: Session = Depends(get_db)):
    return get_all_dosen(db)

@router.get("/{inisial}", response_model=DosenResponseSchema)
def get_dosen_route(inisial: str, db: Session = Depends(get_db)):
    
    data = get_dosen(db, inisial)
    if not data:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    waktu_bimbingan = get_waktu_bimbingan_from_dosen(db, inisial)
    
    return JSONResponse (content={
        "dosen": {
            "nomor_induk": data.nomor_induk,
            "name": data.name,
            "alias": data.alias,
            "email": data.email,
            "status_kehadiran": data.status_kehadiran,
            "keterangan": data.keterangan
        },
        "waktu_bimbingan": [
            {
                "bimbingan_id": item.bimbingan_id,
                "tanggal": str(item.tanggal),
                "waktu_mulai": str(item.waktu_mulai),
                "waktu_selesai": str(item.waktu_selesai),
                "lokasi": item.lokasi,
                "keterangan": item.keterangan
            }
            for item in waktu_bimbingan
        ]
    })

@router.put("/{inisial}")
async def update_dosen_route(inisial: str, dosen_data: DosenUpdateSchema, db: Session = Depends(get_db)):
    dosen = update_dosen(db, inisial, dosen_data)
    if not dosen:
        raise HTTPException(status_code = 404, detail = "Dosen Tidak Ditemukan")
    return {
        "Message": "Dosen Telah diUpdate", 
        "data":jsonable_encoder(DosenResponseSchema.model_validate(dosen))
    }

@router.get("/admin/all", response_model=list[DosenSchema], dependencies=[Depends(require_roles("admin"))])
def get_all_dosen_admin_route(db: Session = Depends(get_db)):
    return get_all_dosen(db)

@router.get("/admin/{dosen_id}", response_model=DosenResponseSchema, dependencies=[Depends(require_roles("admin"))])
def get_dosen_detail_route(dosen_id: UUID, db: Session = Depends(get_db)):
    return get_detail_dosen(db, dosen_id)

@router.delete("/{dosen_id}", dependencies=[Depends(require_roles("admin"))])
def delete_dosen_route(dosen_id: UUID, db: Session = Depends(get_db)):
    return delete_dosen(db, dosen_id)

@router.patch("/u/s/{dosen_alias}")
async def update_kehadiran_dosen(dosen_alias: str, status: str = None, db: Session = Depends(get_db)):
    dosen = set_kehadiran_dosen(db, dosen_alias, status)
    if not dosen:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")
    return {
        "message": f"Dosen {dosen_alias} telah diupdate kehadirannya."
    }

@router.patch("/t/u/status")
async def test_update_Status_kehadiran_route(db: Session = Depends(get_db)):
    return await update_dosen_status(db)

@router.get("/attendance/{dosen_inisial}", response_model=list[AttendanceLogSchema])
def get_dosen_attendance_route(dosen_inisial: str, db: Session = Depends(get_db)):
    attendance_logs = get_dosen_attendance_logs(db, dosen_inisial)
    if not attendance_logs:
        raise HTTPException(status_code=404, detail="Attendance logs not found for this dosen.")
    return attendance_logs

@router.get("/attendance-all/", response_model=list[AttendanceLogSchema])
def get_all_dosen_attendance_route(db: Session = Depends(get_db)):
    attendance_logs = get_all_dosen_attendance_logs(db)
    if not attendance_logs:
        raise HTTPException(status_code=404, detail="No attendance logs found.")
    return attendance_logs