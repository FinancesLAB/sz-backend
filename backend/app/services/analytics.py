from datetime import datetime, timedelta
from locale import currency
from turtle import position

from asyncpg import StringDataLengthMismatchError
from shared.repositories.asset_price import AssetPriceRepository
from shared.repositories.portfolio import PortfolioRepository
from shared.repositories.asset import AssetRepository
from shared.repositories.portfolio_position import PortfolioPositionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.analytics import PortfolioShapshotResponse, TopPosition, SectorDistributionResponse, SectorPositions
class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.asset_price_repo=AssetPriceRepository(session=session)
        self.portfolio_repo=PortfolioRepository(session=session)
        self.portfolio_position_repo=PortfolioPositionRepository(session=session)
        self.asset_repo=AssetRepository(session=session)

    async def portfolio_snapshot(self, portfolio_id: int): # рассмотреть сырыe sql запросы для аналитики и свой репо
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None: raise HTTPException(404, "SZ portfolio not found")
        positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id)
        if not positions: return PortfolioShapshotResponse(portfolio_id=portfolio_id, 
                                                           name=portfolio.name,
                                                           total_value=0,
                                                           total_profit=0,
                                                           total_profit_percent=0,
                                                           invested_value=0,
                                                           currency=portfolio.currency,
                                                           positions_count=0,
                                                           top_positions=[])
        total_value = int()
        asset_ids=[pos.asset_id for pos in positions]
        prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
        
        total_value = sum(pos.quantity * prices[pos.asset_id] for pos in positions)
        invested_value = sum(pos.avg_price * pos.quantity for pos in positions)
        total_profit = total_value - invested_value
        total_profit_percent = total_profit / invested_value * 100
        positions_count=len(positions)
        assets = await self.asset_repo.get_assets_dict_by_ids(asset_ids)
        tops=list()
        for pos in positions:
            new_top = TopPosition(
                asset_id=pos.asset_id,
                ticker=assets[pos.asset_id].ticker,
                full_name=assets[pos.asset_id].full_name,
                quantity=pos.quantity,
                avg_buy_price=pos.avg_price,
                current_price=prices[pos.asset_id],
                current_value=pos.quantity * prices[pos.asset_id],
                profit=pos.quantity * prices[pos.asset_id] - pos.quantity * pos.avg_price,
                profit_percent = ((prices[pos.asset_id] - pos.avg_price) / pos.avg_price) * 100,
                weight_percent=((pos.quantity * prices[pos.asset_id])/total_value) * 100
            )
            tops.append(new_top)
        tops = sorted(tops, key=lambda pos: pos.current_value, reverse=True)
        top_three=tops[:3]

        return PortfolioShapshotResponse(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            total_value=total_value,
            total_profit=total_profit,
            total_profit_percent=total_profit_percent,
            invested_value=invested_value,
            currency=portfolio.currency,
            positions_count=positions_count,
            top_positions=top_three

        )
    


    
    async def sector_distribution(self, portfolio_id):
        sectors = ["energy", "finance", "retail", "transport", "metals", "it", "construction", "industrial", "telecom", "agro", "healthcare"]
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None: raise HTTPException(404, "SZ portfolio not found")
        positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id)
        if not positions: return SectorDistributionResponse(portfolio_id=portfolio_id,
                                                            total_value=0,
                                                            sectors=[])
        asset_ids=[pos.asset_id for pos in positions]
        prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
        total_value = sum(pos.quantity * prices[pos.asset_id] for pos in positions)
        assets = await self.asset_repo.get_assets_dict_by_ids(asset_ids)
        
        sector_to_current_value = dict.fromkeys(sectors, 0)
        for pos in positions:
            sector_to_current_value[assets[pos.asset_id].sector] += (prices[pos.asset_id] * pos.quantity)
        sector_positions = []
        for sector in sectors:
            sector_pos = SectorPositions(sector=sector, 
                            current_value=sector_to_current_value[sector], 
                            weight_percent=(sector_to_current_value[sector]/total_value)*100)
            sector_positions.append(sector_pos)
        

        return SectorDistributionResponse(
            portfolio_id=portfolio_id,
            total_value=total_value,
            sectors=sector_positions
        )



    async def positions_breakdown(self, portfolio_id):
        pass
    

    async def portfolios_dynamics(self, user_id: int):
        portfolios = await self.portfolio_repo.get_by_user_id(user_id=user_id)
        since = datetime.utcnow() - timedelta(hours=24)
        response = []
        for portfolio in portfolios:
            positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id=portfolio.id)
            if not positions:
                response.append({"id": portfolio.id, "name": portfolio.name, "data": []})
                continue

            asset_ids = [p.asset_id for p in positions]
            pos_dict = {p.asset_id: p.quantity for p in positions}

            prices = await self.asset_price_repo.get_prices_since(ids=asset_ids, since=since)

            time_map = {}
            for price in prices:
                ts = price.timestamp
                asset_id = price.asset_id
                if ts not in time_map: time_map[ts] = 0
                time_map[ts] += price.price * pos_dict[asset_id]
            
            data = [{"timestamp": ts.isoformat(), "value": float(val)}
                    for ts, val in sorted(time_map.items(), key=lambda x: x[0])
            ]
            
            response.append({
                "id" : portfolio.id,
                "name" : portfolio.name,
                "data" : data
            })
            
        return response
