from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services.admin import create_admin, get_admin_by_id
from app.schemas.admin import AdminSchema

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AdminSchema)
def create_admin_route(admin: AdminSchema, db: Session = Depends(get_db)):
    return create_admin(db, admin)

@router.get("/{account_id}", response_model=AdminSchema)
def get_admin_route(account_id: int, db: Session = Depends(get_db)):
    return get_admin_by_id(db, account_id)
