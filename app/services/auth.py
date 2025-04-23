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

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    userID = user.user_id

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    
    token = create_access_token(
        data={
            "sub": str(userID),
            "role": user.role
        },
        expires_delta=timedelta(minutes=60)
    )

    response_data = {
        "access_token": token,
        "token_type": "bearer"
    }

    return response_data

    # response_data = {
    #     "access_token": token,
    #     "token_type": "bearer",
    #     "user": {
    #         "user_id": str(userID),
    #         "email": user.email,
    #         "role": user.role,
    #         "profile": {}
    #     }
    # }

    # if user.role == "admin":
    #     admin = db.query(Admin).filter(Admin.id == userID).first()
    #     if admin:
    #         response_data["user"]["profile"] = {
    #             "name": admin.name
    #         }

    # elif user.role == "dosen":
    #     dosen = db.query(Dosen).filter(Dosen.id == userID).first()
    #     if dosen:
    #         response_data["user"]["profile"] = {
    #             "name": dosen.name,
    #             "inisial": dosen.alias
    #         }

    # elif user.role == "mahasiswa":
    #     mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == userID).first()
    #     if mahasiswa:
    #         response_data["user"]["profile"] = {
    #             "name": mahasiswa.nama,
    #             "nim": mahasiswa.nim
    #         }

    # return response_data


    # if user.role == "mahasiswa":
    #     mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == user.id).first()
    #     if mahasiswa:
    #         response_data["mahasiswa"] = {
    #             "nim": mahasiswa.nim,
    #             "name": mahasiswa.nama,
    #             "topik_penelitian": mahasiswa.topik_penelitian
    #         }
    # elif user.role == "dosen":
    #     dosen = db.query(Dosen).filter(Dosen) 

    


    # user = db.query(User).filter(User.email == email).first()
    # if not user or not verify_password(password, user.password):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Invalid Credentials"
    #     )
    
    # token = create_access_token(
    #     data={
    #         "sub": user.email,
    #         "role": user.role
    #     },
    #     expires_delta=timedelta(minutes=60)
    # )

    # return {
    #     "access_token": token,
    #     "token_type": "bearer",
    #     "role": user.role
    # }

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