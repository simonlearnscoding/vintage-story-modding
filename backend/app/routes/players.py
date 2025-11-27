from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PlayerCreate,
    PlayerResponse,
    UserLogResponse,
    PlayerJoinRequest,
    PlayerLeaveRequest,
)
from app.services.player_service import PlayerService

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerResponse)
async def create_player(player: PlayerCreate):
    try:
        created_player = PlayerService.create_player(player.uid, player.name)
        return created_player
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs", response_model=list[UserLogResponse])
async def get_all_player_logs():
    try:
        logs = PlayerService.get_all_player_logs()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{uid}/logs", response_model=list[UserLogResponse])
async def get_player_logs(uid: str):
    try:
        logs = PlayerService.get_player_logs(uid)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{uid}", response_model=PlayerResponse)
async def get_player(uid: str):
    player = PlayerService.get_player(uid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/", response_model=list[PlayerResponse])
async def get_all_players():
    try:
        players = PlayerService.get_all_players()
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/join", response_model=PlayerResponse)
async def join_player(join_request: PlayerJoinRequest):
    try:
        # Upsert player
        player = PlayerService.create_player(
            join_request.PlayerUID, join_request.LastKnownPlayername
        )

        # Create user log
        PlayerService.create_user_log(join_request.PlayerUID, join_request.LastJoinDate)

        return player
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/leave")
async def leave_player(leave_request: PlayerLeaveRequest):
    try:
        # Update existing log with leave time
        updated_log = PlayerService.update_user_log_with_leave_time(
            leave_request.uid, leave_request.leftAt
        )

        if not updated_log:
            raise HTTPException(
                status_code=404, detail="No active join log found for player"
            )

        return {"message": "Player leave recorded successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
