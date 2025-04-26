from fastapi import UploadFile
from mimetypes import guess_type

from sqlalchemy.orm import Session

from app.models.file import Files
from app.schemas.file import FileSchema
from app.utils.supabase_client import *
# from app.utils.constant import *

from uuid import uuid4

def upload_file(file: UploadFile) -> str:
    file_ext = file.filename.split('.')[-1]    
    unique_filename = f"{uuid4()}_{file.filename}"
    content_type = guess_type(file.filename)[0] or "application/octet-stream"
    
    file_bytes = file.file.read()
    
    supabase.storage.from_(BUCKET_NAME).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={
            "content-type": content_type,
            "cache-control" : "3600"       
        }
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    return public_url

def get_files(db: Session, student_id: str):
    return db.query(Files).filter(Files.mahasiswa_nim == student_id).all()