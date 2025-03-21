from pydantic import BaseModel

class NewsSchema(BaseModel):
    title: str
    content: str
    admin_id: int

    class Config:
        from_attributes = True