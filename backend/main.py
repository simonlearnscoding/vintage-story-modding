from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api, health, players

app = FastAPI(
    title="VS Modding API",
    description="API for Vintage Story modding project",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(health.router)
app.include_router(players.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)