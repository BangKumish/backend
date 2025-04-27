from sqlalchemy import Column 
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from app.config import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    # is_active = Column(Boolean, nullable=False, default=False)
