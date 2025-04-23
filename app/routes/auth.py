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

# @router.post("/register")
# def register(user_data: RegisterUser, db: Session = Depends(get_db)):
#     return register_user(db, user_data)
