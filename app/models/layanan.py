from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base
from datetime import datetime

class Layanan(Base):
    __tablename__ = "layanan"

    layanan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    layanan_jenis = Column(String, nullable=False)
    layanan_file = Column(String, unique=True, nullable=False)
    layanan_status = Column(Integer,default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
