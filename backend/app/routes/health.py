from fastapi import APIRouter
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    return HealthService.get_status()