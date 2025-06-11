from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Relationship

from app.database.session import Base

from datetime import datetime

class AttendanceLog(Base):
    __tablename__ = "attendance_log"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    dosen_inisial = Column(String, ForeignKey("dosen.alias", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    dosen_nama = Column(String, nullable=False)
    tanggal = Column(Date, default=datetime.date, nullable=False)
    status_kehadiran = Column(Boolean, nullable=False, default=True)
    keterangan = Column(String, default="", nullable=True)

    dosen = Relationship("Dosen", back_populates="attendance_logs")