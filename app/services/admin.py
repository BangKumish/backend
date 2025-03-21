from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminSchema
from app.utils.security import hash_password

def create_admin(db: Session, admin: AdminSchema):
    db_admin = Admin(
        name = admin.name,
        email = admin.email,
        password = hash_password(admin.password)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin_by_id(db: Session, account_id: int):
    return db.query(Admin).filter(Admin.account_id == account_id).first()

def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()
