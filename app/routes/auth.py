from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.services.auth import *
from app.schemas.user import *
from app.utils.dependencies import *

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(login_data: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)

@router.post("/register")
def register(user_data: RegisterUser, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.get("/me", response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    return current_user()

@router.put("/me", response_model=UserResponse)
def update_my_profile(profile_data: UpdateProfile, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return update_profile(current_user.id, profile_data, db)