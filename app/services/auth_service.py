from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException

from app.utils.security import *

from app.models.admin import Admin
from app.models.dosen import Dosen
from app.models.mahasiswa import Mahasiswa
from app.models.user import User

from app.schemas.user import *

# =============================================================== #
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# LOGIN 
def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    userID = user.user_id    
    token = create_access_token(
        data={
            "sub": str(userID),
            "role": user.role
        },
        expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_user_profile(user: User, db: Session) -> UserProfileResponse:
    if user.role == "admin":
        admin = db.query(Admin).filter(Admin.id == user.user_id).first()
        profile = AdminProfile(role="admin", name=admin.name, email=admin.email)
    elif user.role == "dosen":
        dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
        profile = DosenProfile(role="dosen", name=dosen.name, alias=dosen.alias, email=dosen.email)
    elif user.role == "mahasiswa":
        mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
        profile = MahasiswaProfile(role="mahasiswa", name=mhs.nama, nim=mhs.nim, email=mhs.email)
    
    return UserProfileResponse(
        user_id=user.user_id,
        email=user.email,
        role=user.role,
        profile=profile
    )

def decode_token(token: str, db: Session):
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

    return user

