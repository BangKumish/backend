from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.admin import create_admin, get_admin_by_id
from app.schemas.admin import *

from uuid import UUID

from app.config import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/", response_model=AdminSchema)
def create_admin_route(admin: AdminCreateSchema, db: Session = Depends(get_db)):
    return create_admin(db, admin)

@router.get("/{admin_id}", response_model=AdminSchema)
def get_admin_route(admin_id: UUID, db: Session = Depends(get_db)):
    return get_admin_by_id(db, admin_id)
