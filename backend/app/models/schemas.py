from pydantic import BaseModel
from typing import Optional

class PlayerCreate(BaseModel):
    uid: str
    name: str

class PlayerResponse(BaseModel):
    uid: str
    name: str
    
    class Config:
        from_attributes = True

class UserLogCreate(BaseModel):
    uid: str
    joinedAt: str
    leftAt: Optional[str] = None