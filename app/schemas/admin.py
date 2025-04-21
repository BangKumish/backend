from pydantic import BaseModel
from uuid import UUID
class AdminSchema(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    
    class Config:
        from_attributes = True

class AdminCreateSchema(BaseModel):
    name: str
    email: str
    password: str