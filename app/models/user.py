from sqlalchemy import Boolean, Column, DateTime, String 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Relationship
from datetime import datetime
from app.config import Base

import uuid

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    # is_active = Column(Boolean, nullable=False, default=False)

    # admin = Relationship("Admin", back_populates="user", uselist=False)
    # dosen = Relationship("Dosen", back_populates="user", uselist=False)
    # mahasiswa = Relationship("Mahasiswa", back_populates="user", uselist=False)