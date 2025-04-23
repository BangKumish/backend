from fastapi import APIRouter, Depends
from fastapi import Query
from jwt import PyJWKError
from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.services.auth import *
from app.schemas.user import *
from app.utils.dependencies import *

from app.config import get_db
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login")
def login_route(login_data: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)

@router.get("/me")
def get_profile_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = {}

    if user.role == "admin":
        admin = db.query(Admin).filter(Admin.id == user.user_id).first()
        if admin:
            profile = {
                "role": "admin",
                "name": admin.name,
                "email": admin.email
            }

    elif user.role == "dosen":
        dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
        if dosen:
            profile = {
                "role": "dosen",
                "name": dosen.name,
                "alias": dosen.alias,
                "email": dosen.email
            }

    elif user.role == "mahasiswa":
        mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
        if mhs:
            profile = {
                "role": "mahasiswa",
                "name": mhs.nama,
                "nim": mhs.nim,
                "email": mhs.email
            }

    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "profile": profile
    }

@router.get("/test-me")
def get_me_test(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired")

    user = db.query(User).filter(User.user_id == UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == "admin":
        admin = db.query(Admin).filter(Admin.id == user.user_id).first()
        if admin:
            profile = {
                "role": "admin",
                "name": admin.name,
                "email": admin.email
            }

    elif user.role == "dosen":
        dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
        if dosen:
            profile = {
                "role": "dosen",
                "name": dosen.name,
                "alias": dosen.alias,
                "email": dosen.email
            }

    elif user.role == "mahasiswa":
        mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
        if mhs:
            profile = {
                "role": "mahasiswa",
                "name": mhs.nama,
                "nim": mhs.nim,
                "email": mhs.email
            }

    return profile

