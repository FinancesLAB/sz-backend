from fastapi import APIRouter, status, Depends
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse, PortfolioUpdate
from app.services.portfolios import PortfolioService
from app.api.deps import get_porfolio_service
router = APIRouter(prefix="/portfolios", tags=["Portfolios"])

@router.get("/admin/{portfolio_id}")
async def get_by_id(portfolio_id: int, service: PortfolioService=Depends(get_porfolio_service)) -> PortfolioResponse:
    return await service.get_portfolio_by_portfolio_id(portfolio_id=portfolio_id)

@router.get("/admin")
async def get_all(service: PortfolioService=Depends(get_porfolio_service)) -> list[PortfolioResponse]:
    return await service.get_all_portfolios()

@router.post("/admin")
async def create(payload: PortfolioCreate, service: PortfolioService = Depends(get_porfolio_service)) -> PortfolioResponse:
    return await service.create_portfolio(payload)

@router.delete("/admin/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(portfolio_id: int, service: PortfolioService=Depends(get_porfolio_service)):
    await service.delete_portfolio_by_portfolio_id(portfolio_id=portfolio_id)
    return

@router.patch("/admin/{portfolio_id}")
async def update_portfolio(portfolio_id: int, payload: PortfolioUpdate, service: PortfolioService=Depends(get_porfolio_service)) -> PortfolioResponse:
    return await service.update(portfolio_id=portfolio_id, payload=payload)

@router.get("/admin/user/{user_id}") # add pydantic
async def get_user_portfolios(user_id: int, service: PortfolioService=Depends(get_porfolio_service)):
    return await service.get_user_portfolios(user_id=user_id)
