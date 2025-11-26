from fastapi import APIRouter
from backend.app.core.database import SessionDep
from backend.app.services.analytics import AnalyticsService
router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/users/{user_id}/portfolio/analytics/dynamics")
async def get_dynamics(session: SessionDep, user_id: int):
    return await AnalyticsService.portfolio_dynamics(session, user_id)