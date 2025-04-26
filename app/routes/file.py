from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.models.file import Files as FileModel
from app.services.file_service import *
from app.schemas.file import *
from app.utils.supabase_client import * 

from app.config import get_db

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/", response_model=FileSchema)
async def upload_file(antrian_id: int, mahasiswa_nim: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_url = upload_to_supabase(file)

        file_record = FileModel(
            antrian_id = antrian_id,
            mahasiswa_nim = mahasiswa_nim,
            filename = file.filename,
            file_url = file_url,
            is_checked = False,
            created_at = datetime.now()
        )

        db.add(file_record)
        db.commit()
        db.refresh(file_record)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    return file_record

@router.get("/{file_id}", response_model=FileSchema)
def get_file_route(file_id: UUID, db: Session = Depends(get_db)):
    pass

@router.put("/{file_id}", response_model=FileSchema)
def update_file_route(file_id: UUID, update_data: FileUpdateSchema, db: Session = Depends(get_db)):
    return update_files(db, file_id, update_data)
    