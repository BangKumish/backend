from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.news_service import create_news, get_all_news
from app.schemas.news import NewsSchema
from app.utils.dependencies import get_current_user

from app.config import get_db

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/")
def create_news_route(news_data: NewsSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only Admin can Post")
    return create_news(db, news_data)

@router.get("/")
def get_news_route(db: Session = Depends(get_db)):
    return get_all_news(db)