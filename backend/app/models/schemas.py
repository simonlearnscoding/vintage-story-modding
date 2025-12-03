from pydantic import BaseModel
from typing import Optional


class PlayerCreate(BaseModel):
    uid: str
    name: str

class PlayerJoinRequest(BaseModel):
    PlayerUID: str
    LastKnownPlayername: str
    LastJoinDate: str

class PlayerLeaveRequest(BaseModel):
    PlayerUID: str
    leftAt: str

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
    name: str
    joinedAt: str
    leftAt: Optional[str] = None

    class Config:
        from_attributes = True

class PlayerDetailsResponse(BaseModel):
    name: str
    uid: str
    isOnline: bool
    onlineSince: Optional[str] = None
    lastOnline: Optional[str] = None

class PlayerDeathInfo(BaseModel):
    PlayerUID: str
    damageSource: str
    deathTime:str