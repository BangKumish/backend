from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException, Depends

from app.utils.security import *
from app.config import SessionLocal

from app.models.admin import Admin
from app.models.mahasiswa import Mahasiswa
from app.models.dosen import Dosen
from app.models.user import User
from app.schemas.user import *

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
# def login_user(db: Session, email:str, password:str):
#     user = authenticate_user(db, email, password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid email or password")
#     access_token = create_access_token({"sub": user.email, "role": user.__tablename__}, timedelta(minutes=60))
#     return {"access_token": access_token, "token_type": "bearer", "role": user.__tablename__}

def register_user(db: Session, user_data: RegisterUser):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    user = User(
        email = user_data.email,
        password = hash_password(user_data.password),
        role = user_data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    
    token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        },
        expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }

def update_profile(user_id: str, profile_date: UpdateProfile, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not User:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    
    for key, value in profile_date.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user