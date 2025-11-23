
from fastapi import FastAPI
from app.routers import users, assets
app = FastAPI()
app.include_router(users.router)
app.include_router(assets.router)

