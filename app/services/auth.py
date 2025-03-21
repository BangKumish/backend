from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException, Depends
from app.utils.security import verify_password, create_access_token
from app.config import SessionLocal
from app.models.admin import Admin
from app.models.mahasiswa import Mahasiswa
from app.models.dosen import Dosen

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authenticate User
def authenticate_user(db: Session, email:str, password:str):
    user = db.query(Admin).filter(Admin.email == email).first() or \
           db.query(Dosen).filter(Dosen.email == email).first() or \
           db.query(Mahasiswa).filter(Mahasiswa.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return None
    
    return user

# Login Function
def login_user(db: Session, email:str, password:str):
    user = authenticate_user(db, email, password)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.email, "role": user.__tablename__}, timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer", "role": user.__tablename__}
