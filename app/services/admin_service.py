from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.models.user import User
from app.schemas.admin import *
from app.utils.security import hash_password

from uuid import UUID

import uuid

def create_admin(db: Session, admin: AdminSchema):
    hashed_password = hash_password(admin.password)
    admin_id = uuid.uuid4()
    
    db_admin = Admin(
        id = admin_id,
        name = admin.name,
        email = admin.email,
        password = hashed_password
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    db_user = User(
        user_id = admin_id,
        email = admin.email,
        password = hashed_password,
        role = "admin"
    )

    db.add(db_user)
    db.commit()

    return db_admin

def get_admin_by_id(db: Session, admin_id: UUID):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()

def get_all_admin(db: Session):
    return db.query(Admin).order_by(Admin.name.asc()).all()

def update_admin(db: Session, admin_id: UUID, data: AdminUpdateSchema):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    
    if not admin:
        return None
    
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(admin, key, value)

    db.commit()
    db.refresh(admin)
    return admin

def delete_admin(db: Session, admin_id: UUID):
    data = db.query(Admin).filter(Admin.id == admin_id).first()
    if data:
        db.delete(data)
        db.commit()
    return data
    