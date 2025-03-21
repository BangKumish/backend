from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services.file import get_files, upload_file
from app.schemas.file import FileSchema
from app.utils.dependencies import get_current_user
import shutil

router = APIRouter(prefix="/file", tags=["File"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_FOLDER = "uploads/"

@router.post("/")
def upload_file_route(
    student_id: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user)
    ):
    if user["role"] != "mahasiswa":
        raise HTTPException(status_code=403, detail="Only Student can Post")
    
    file_path = f"{UPLOAD_FOLDER}{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_data = FileSchema(
        filename=file.filename,
        file_url=file_path,
        student_id=student_id
    )
    return upload_file(db, file_data)

@router.get("/{student_id}")
def get_file_route(student_id: str, db: Session = Depends(get_db), user:dict = Depends(get_current_user)):
    if user["role"] != "admin" and user["role"] != "mahasiswa":
        raise HTTPException(status_code=403, detail="Only Students and Admin can view files")
    return get_files(db, student_id)