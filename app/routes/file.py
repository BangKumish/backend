from fastapi import APIRouter, UploadFile, File
from app.services.file import *

from app.config import get_db

router = APIRouter(prefix="/file", tags=["File"])

UPLOAD_FOLDER = "uploads/"

# @router.post("/upload")
# def upload_lampiran(file: UploadFile = File(...)):
#     file_url = upload_file(file)  # pastikan fungsi upload_file benar
#     return {
#         "message": "Upload Berhasil",
#         "url": file_url,
#     }

# @router.post("/")
# def upload_file_route(
#     student_id: str, 
#     file: UploadFile = File(...), 
#     db: Session = Depends(get_db), 
#     user: dict = Depends(get_current_user)
#     ):
#     if user["role"] != "mahasiswa":
#         raise HTTPException(status_code=403, detail="Only Student can Post")
    
#     file_path = f"{UPLOAD_FOLDER}{file.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     file_data = FileSchema(
#         filename=file.filename,
#         file_url=file_path,
#         student_id=student_id
#     )
#     return upload_file(db, file_data)

# @router.get("/{student_id}")
# def get_file_route(student_id: str, db: Session = Depends(get_db), user:dict = Depends(get_current_user)):
#     if user["role"] != "admin" and user["role"] != "mahasiswa":
#         raise HTTPException(status_code=403, detail="Only Students and Admin can view files")
#     return get_files(db, student_id)