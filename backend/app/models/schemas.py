from pydantic import BaseModel
from typing import Optional

class PlayerCreate(BaseModel):
    uid: str
    name: str

class PlayerJoinRequest(BaseModel):
    uid: str
    name: str
    joinedAt: str

class PlayerResponse(BaseModel):
    uid: str
    name: str
    
    class Config:
        from_attributes = True

class UserLogCreate(BaseModel):
    uid: str
    joinedAt: str
    leftAt: Optional[str] = None

class UserLogResponse(BaseModel):
    id: int
    uid: str
    joinedAt: str
    leftAt: Optional[str] = None
    
    class Config:
        from_attributes = True