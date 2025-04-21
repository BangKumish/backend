from sqlalchemy import Boolean, Column, DateTime, String 
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.config import Base

import uuid

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    ktm_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
