from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from datetime import datetime
from app.config import Base

class File(Base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP, default=datetime.now())
    student_id = Column(String, ForeignKey("mahasiswa.nim"), nullable=False)
    