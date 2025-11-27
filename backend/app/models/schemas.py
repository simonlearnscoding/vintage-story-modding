from pydantic import BaseModel
from typing import Optional


class PlayerCreate(BaseModel):
    uid: str
    name: str

class PlayerJoinRequest(BaseModel):
    PlayerUID: str
    RoleCode: str
    PermaPrivileges: list
    DeniedPrivileges: list
    PlayerGroupMemberShips: dict
    AllowInvite: bool
    LastKnownPlayername: str
    CustomPlayerData: dict
    ExtraLandClaimAllowance: int
    ExtraLandClaimAreas: int
    FirstJoinDate: str
    LastJoinDate: str
    LastCharacterSelectionDate: str

class PlayerLeaveRequest(BaseModel):
    uid: str
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