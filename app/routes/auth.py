from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.services.auth import *
from app.schemas.user import *
from app.utils.dependencies import *

from app.config import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(login_data: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)

@router.get("/me")
def get_my_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile_data = {
        "user_id": str(user.user_id),
        "email": user.email,
        "role": user.role
    }

    if user.role == "admin":
        admin = db.query(Admin).filter(Admin.id == user.user_id).first()
        profile_data["admin"] = {
            "name": admin.name,
            "email": admin.email
        } if admin else None

    elif user.role == "dosen":
        dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
        profile_data["dosen"] = {
            "name": dosen.name,
            "alias": dosen.alias,
            "email": dosen.email
        } if dosen else None

    elif user.role == "mahasiswa":
        mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
        profile_data["mahasiswa"] = {
            "nim": mhs.nim,
            "nama": mhs.nama
        } if mhs else None

    return profile_data

# @router.post("/register")
# def register(user_data: RegisterUser, db: Session = Depends(get_db)):
#     return register_user(db, user_data)
