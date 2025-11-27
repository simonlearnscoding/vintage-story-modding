from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/")
async def api_root():
    return {"message": "VS Modding API is running"}