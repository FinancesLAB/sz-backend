from typing import List, Dict
from datetime import datetime, timedelta
from shared.models.asset_price import AssetPrice
from shared.repositories.asset_price import AssetPriceRepository
from shared.repositories.portfolio import PortfolioRepository
from shared.repositories.asset import AssetRepository
from shared.repositories.portfolio_position import PortfolioPositionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.analytics import PortfolioShapshotResponse, TopPosition, SectorDistributionResponse, SectorPosition, PortfolioPrice, PortfolioDynamicsResponse
from app.analytics.portfolio_snapshot import (
    calc_portfolio_current_value,
    calc_invested_value,
    calc_profit,
    calc_portfolio_profit_percent,
    calc_position_current_value,
    calc_position_profit,
    calc_position_profit_percent,
    calc_position_weight_in_portfolio,
)
from app.analytics.portfolio_dynamics import get_timestamps_count_24h, get_sorted_timeseries_24h, get_portfolio_price_by_ts

        
class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.asset_price_repo=AssetPriceRepository(session=session)
        self.portfolio_repo=PortfolioRepository(session=session)
        self.portfolio_position_repo=PortfolioPositionRepository(session=session)
        self.asset_repo=AssetRepository(session=session)

    async def portfolio_snapshot(self, portfolio_id: int) -> PortfolioShapshotResponse: # рассмотреть сырыe sql запросы для аналитики и свой репо
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None: 
            raise HTTPException(404, "SZ portfolio not found")
        positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id)
        if not positions: 
            return PortfolioShapshotResponse.empty(portfolio)
        asset_ids=[pos.asset_id for pos in positions]
        current_prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
        total_value = calc_portfolio_current_value(positions=positions, current_prices=current_prices)
        invested_value = calc_invested_value(positions=positions)
        total_profit = calc_profit(current_value=total_value, invested_value=invested_value)
        total_profit_percent = calc_portfolio_profit_percent(profit=total_profit, invested_value=invested_value)
        assets = await self.asset_repo.get_assets_dict_by_ids(asset_ids)
        tops=list()
        for pos in positions:
            new_top = TopPosition(
                asset_id=pos.asset_id,
                ticker=assets[pos.asset_id].ticker,
                full_name=assets[pos.asset_id].full_name,
                quantity=pos.quantity,
                avg_buy_price=pos.avg_price,
                current_price=current_prices[pos.asset_id],
                current_value=calc_position_current_value(position=pos, current_prices=current_prices),
                profit=calc_position_profit(position=pos, current_prices=current_prices),
                profit_percent = calc_position_profit_percent(position=pos, current_prices=current_prices),
                weight_percent=calc_position_weight_in_portfolio(position=pos, current_prices=current_prices, total_value=total_value)
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
            positions_count=len(positions),
            top_positions=top_three

        )
    

    async def sector_distribution(self, portfolio_id: int) -> SectorDistributionResponse:
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ portfolio not found")
        positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id)
        if not positions:
            return SectorDistributionResponse.empty(portfolio)
        asset_ids=[pos.asset_id for pos in positions]
        prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
        total_value = sum(pos.quantity * prices[pos.asset_id] for pos in positions)
        assets = await self.asset_repo.get_assets_dict_by_ids(asset_ids)
        sector_to_value={}
        for pos in positions:
            sec=assets[pos.asset_id].sector
            value=prices[pos.asset_id] * pos.quantity
            sector_to_value[sec]  = sector_to_value.get(sec, 0) + value
        sector_positions = []
        for sector in sector_to_value.keys():
            sector_positions.append(SectorPosition(sector=sector, 
                            current_value=sector_to_value[sector], 
                            weight_percent=(sector_to_value[sector]/total_value)*100))
        sector_positions.sort(key=lambda x: x.current_value, reverse=True)
        return SectorDistributionResponse(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            total_value=total_value,
            currency=portfolio.currency,
            sectors=sector_positions
        )


    async def positions_breakdown(self, portfolio_id):
        pass
    

    async def portfolio_dynamics_for_24h(self, portfolio_id: int) -> PortfolioDynamicsResponse:
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id=portfolio_id)
        if portfolio is None:
            raise HTTPException(404, "SZ portfolio not found")
        positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id=portfolio_id)
        if not positions:
            return PortfolioDynamicsResponse.empty(portfolio=portfolio)

        timestamp_now = datetime.utcnow()
        asset_ids = [pos.asset_id for pos in positions]

        asset_prices = await self.asset_price_repo.get_prices_since(ids=asset_ids, since=timestamp_now - timedelta(days=1) )
        
        timestamps_count = get_timestamps_count_24h(ts_now=timestamp_now)
        time_series = get_sorted_timeseries_24h(ts_now=timestamp_now, count=timestamps_count)
        asset_id_to_quantity = {}
        for pos in positions:
            asset_id_to_quantity[pos.asset_id] = pos.quantity
        data = []
        for ts in time_series:
            data.append(PortfolioPrice(timestamp=ts, total_value=get_portfolio_price_by_ts(ts, asset_prices, asset_id_to_quantity)))
        
        return PortfolioDynamicsResponse(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            data=data
        )