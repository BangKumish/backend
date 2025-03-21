from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services.auth import login_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginScheme(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(login_data: LoginScheme, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)