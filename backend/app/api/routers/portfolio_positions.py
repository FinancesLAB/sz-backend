from fastapi import APIRouter, Depends, status
from app.schemas.portfolio_position import PortfolioPositionCreate, PortfolioPositionResponse, PrettyPortfolioPosition
from app.services.portfolio_positions import PortfolioPositionService, PortfolioPositionUpdate
from app.api.deps import get_porfolio_position_service
from typing import List
router = APIRouter(prefix="/portfolio_positions", tags=["Portfolio Positions"])


@router.get("/{portfolio_position}")
async def get_portfolio_position(portfolio_position_id: int, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    return await service.get_by_id(
        portfolio_position_id=portfolio_position_id
    )

@router.get("/")
async def get_portfolio_positions(service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    return await service.get_all()

@router.post("/", response_model=PortfolioPositionResponse)
async def create_portfolio_position(payload: PortfolioPositionCreate, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    return await service.create(payload)

# @router.get("/portfolio/{portfolio_id}")
# async def get_positions_by_portfolio_id(portfolio_id: int, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
#     return await service.get_by_portfolio_id(portfolio_id=portfolio_id)

@router.get("/portfolio/{portfolio_id}", response_model=List[PrettyPortfolioPosition])
async def get_positions_by_portfolio_id(portfolio_id: int, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    return await service.get_by_portfolio_id(portfolio_id=portfolio_id)


@router.delete("/{portfolio_position}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(portfolio_position_id: int, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    await service.delete(
        portfolio_position_id=portfolio_position_id
    )
    return

@router.patch("/{portfolio_position_id}", response_model=PortfolioPositionResponse)
async def update_portfolio_position(portfolio_position_id: int, payload: PortfolioPositionUpdate, service: PortfolioPositionService=Depends(get_porfolio_position_service)):
    return await service.update(portfolio_position_id=portfolio_position_id, payload=payload)
