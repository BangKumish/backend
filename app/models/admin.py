from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base
from datetime import datetime

class Admin(Base):
    __tablename__ = "admin"

    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)
