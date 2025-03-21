from sqlalchemy.orm import Session
from app.models.file import File
from app.schemas.file import FileSchema

def upload_file(db: Session, file_data: FileSchema):
    new_file = File(**file_data.dict())
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def get_files(db: Session, student_id: str):
    return db.query(File).filter(File.student_id == student_id).all()