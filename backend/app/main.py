
from fastapi import FastAPI
from app.routers import users, assets, portfolios
app = FastAPI()
app.include_router(users.router)
app.include_router(assets.router)
app.include_router(portfolios.router)
