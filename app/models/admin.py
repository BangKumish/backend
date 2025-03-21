from sqlalchemy import Column, Integer, String
from app.config import Base

class Admin(Base):
    __tablename__ = "admin"

    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
