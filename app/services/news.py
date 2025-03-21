from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news import NewsSchema

def create_news(db: Session, news_data: NewsSchema):
    new_news = News(**news_data.dict())
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news

def get_all_news(db: Session):
    return db.query(News).all()