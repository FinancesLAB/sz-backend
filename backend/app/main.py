
from fastapi import FastAPI
from app.api.routers import users, assets, portfolios, portfolio_positions, trades, analytics
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
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

app.include_router(users.router)
app.include_router(assets.router)
app.include_router(portfolios.router)
app.include_router(portfolio_positions.router)
app.include_router(trades.router)
app.include_router(analytics.router)