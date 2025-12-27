from fastapi import FastAPI, APIRouter
from app.api.routers.adm import users, assets, portfolios, trades, analytics, auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(assets.router)
api_router.include_router(portfolios.router)
api_router.include_router(trades.router)
api_router.include_router(analytics.router)

app.include_router(api_router)