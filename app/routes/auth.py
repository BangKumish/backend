from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.auth_service import *
from app.schemas.user import *
from app.utils.dependencies import *

from app.config import get_db
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ---------------------------------------
# POST: /auth/login
# ---------------------------------------
@router.post("/login")
def login_route(login_data: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)

# ---------------------------------------
# GET: /auth/me
# ---------------------------------------
@router.get("/me")
async def get_profile_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_profile(user, db)

# ---------------------------------------
# GET: /auth/test-me (for testing via token param)
# ---------------------------------------
@router.get("/test-me")
def get_me_test(token: str, db: Session = Depends(get_db)):
    user = decode_token(token, db)
    return get_user_profile(user, db)

# ---------------------------------------
# POST: /auth/logout
# ---------------------------------------
@router.post("/logout")
def logout_user():
    # Simply instruct the frontend to delete token
    return {"message": "Logout successful. Please delete token on client side."}
