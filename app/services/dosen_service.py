from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database.models.dosen import Dosen
from app.database.models.user import User
from app.routes.websocket_router import manager 
from app.schemas.dosen import *
from app.schemas.push import PushNotificationPayload
from app.middleware.jwt_handler import hash_password

import asyncio
import uuid

def create_dosen(db: Session, dosen: DosenCreateSchema):
    hashed_password = hash_password(dosen.password)
    dosen_id = uuid.uuid4()

    db_dosen = Dosen(
        id = dosen_id,
        nomor_induk = dosen.nomor_induk,
        name = dosen.name,
        email = dosen.email,
        password = hashed_password,
        status_kehadiran = dosen.status_kehadiran,
        ketersediaan_bimbingan = dosen.ketersediaan_bimbingan,
        alias = dosen.alias,
    )
    db.add(db_dosen)
    db.commit()
    db.refresh(db_dosen)
    
    db_user = User(
        user_id = dosen_id,
        email = dosen.email,
        password =hashed_password,
        role = "dosen"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_dosen

def get_dosen(db: Session, nomor_induk: str):
    return db.query(Dosen).filter(Dosen.alias == nomor_induk).first()

def get_all_dosen(db: Session):
    return db.query(Dosen).order_by(Dosen.name.asc()).all()

def get_detail_dosen(db: Session, dosen_id:UUID):
    return db.query(Dosen).filter(Dosen.id == dosen_id).first()

def update_dosen(db: Session, nomor_induk: str, dosen_data: DosenUpdateSchema):
    dosen = db.query(Dosen).filter(Dosen.alias == nomor_induk).first()
    
    if not dosen:
        return None
    
    update_data = dosen_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(dosen, key, value)

    db.commit()
    db.refresh(dosen)

    if "status_kehadiran" in update_data:
        asyncio.get_event_loop().create_task(manager.broadcast_all({
            "Inisial Dosen": dosen.alias,
            "Nama Dosen": dosen.name,
            "Status Kehadrian": dosen.status_kehadiran
        }))
    
    return dosen

def delete_dosen(db: Session, dosen_id: UUID):
    dosen_data = db.query(Dosen).filter(Dosen.id == dosen_id).first()
    if not dosen_data:
        raise HTTPException(
            status_code=404,
            detail="Dosen not found"
        )

    name = dosen_data.name
    user_data = db.query(User).filter(User.user_id == dosen_id).first()
    if user_data:
        db.delete(user_data)

    db.delete(dosen_data)
    db.commit()

    return {
        "message": f"DOSEN {name} has been removed"
    }