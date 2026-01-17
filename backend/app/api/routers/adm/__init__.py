from .users import router as users_router
from .assets import router as assets_router
from .portfolios import router as portfolios_router
from .trades import router as trades_router
from .analytics import router as analytics_router

routers = [
    users_router,
    assets_router,
    portfolios_router,
    trades_router,
    analytics_router,
]
