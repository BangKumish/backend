from pydantic import BaseModel

class FileSchema(BaseModel):
    filename: str
    file_url: str
    student_id: str

    class Config:
        from_attributes = True