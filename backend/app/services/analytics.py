from typing import List, Dict
from datetime import datetime, timedelta
from shared.models.asset_price import AssetPrice
from shared.repositories.asset_price import AssetPriceRepository
from shared.repositories.portfolio import PortfolioRepository
from shared.repositories.asset import AssetRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.analytics import PortfolioShapshotResponse, TopPosition, SectorDistributionResponse, SectorPosition, PortfolioPrice, PortfolioDynamicsResponse
from app.analytics.portfolio_snapshot import get_portfolio_purchase_price, get_asset_id_to_quantity_dict, calc_unrealized_pnl
from shared.repositories.trade import TradeRepository

class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.asset_price_repo=AssetPriceRepository(session=session)
        self.portfolio_repo=PortfolioRepository(session=session)
        self.asset_repo=AssetRepository(session=session)
        self.trade_repo=TradeRepository(session=session)

    async def get_portfolio_total_price(self, portfolio_id: int):
        trades = await self.trade_repo.get_trades_by_portfolio_id(portfolio_id=portfolio_id)
        total_value = 0
        for trade in trades:
            if trade.direction == "buy":
                total_value += trade.quantity * trade.price
            elif trade.direction == "sell":
                total_value -= trade.quantity * trade.price
        return total_value

    async def portfolio_snapshot(self, portfolio_id: int):
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        trades = await self.trade_repo.get_trades_by_portfolio_id(portfolio_id)
        portfolio_purchase_price = get_portfolio_purchase_price(trades)
        asset_ids = [trade.asset_id for trade in trades]
        asset_ids = set(asset_ids)
        current_prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
        asset_id_to_quantity = get_asset_id_to_quantity_dict(trades)
        current_value = 0
        for asset_id, quantity in asset_id_to_quantity.items():
            current_value += current_prices[asset_id] * quantity
        profit = current_value - portfolio_purchase_price
        count = sum(1 for quantity in asset_id_to_quantity.values() if quantity != 0)
        resp = []
        for asset_id, quantity in asset_id_to_quantity.items():
            ticker = "UNK"
            full_name = "fullname"
            quantity = quantity
            pos = TopPosition(
                asset_id=asset_id,
                ticker=ticker,
                full_name=full_name,
                quantity=quantity,
                avg_buy_price=12,
                current_price=0,
                current_value=0,
                profit=0,
                profit_percent = 0,
                weight_percent=0
            )
            resp.append(pos)
        


        total_profit = calc_unrealized_pnl(portfolio_trades=trades, asset_prices=current_prices)
        return PortfolioShapshotResponse(
            portfolio_id=portfolio.id,
            name=portfolio.name,
            total_value=current_value,
            total_profit=profit,
            total_profit_percent=(profit / portfolio_purchase_price) * 100,
            invested_value=portfolio_purchase_price ,
            currency=portfolio.currency,
            positions_count=count,
            top_positions=resp
        )

#     async def sector_distribution(self, portfolio_id: int) -> SectorDistributionResponse:
#         portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
#         if portfolio is None:
#             raise HTTPException(404, "SZ portfolio not found")
#         positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id)
#         if not positions:
#             return SectorDistributionResponse.empty(portfolio)
#         asset_ids=[pos.asset_id for pos in positions]
#         prices = await self.asset_price_repo.get_prices_dict_by_ids(asset_ids)
#         total_value = sum(pos.quantity * prices[pos.asset_id] for pos in positions)
#         assets = await self.asset_repo.get_assets_dict_by_ids(asset_ids)
#         sector_to_value={}
#         for pos in positions:
#             sec=assets[pos.asset_id].sector
#             value=prices[pos.asset_id] * pos.quantity
#             sector_to_value[sec]  = sector_to_value.get(sec, 0) + value
#         sector_positions = []
#         for sector in sector_to_value.keys():
#             sector_positions.append(SectorPosition(sector=sector, 
#                             current_value=sector_to_value[sector], 
#                             weight_percent=(sector_to_value[sector]/total_value)*100))
#         sector_positions.sort(key=lambda x: x.current_value, reverse=True)
#         return SectorDistributionResponse(
#             portfolio_id=portfolio.id,
#             name=portfolio.name,
#             total_value=total_value,
#             currency=portfolio.currency,
#             sectors=sector_positions
#         )


#     async def positions_breakdown(self, portfolio_id):
#         pass
    

#     async def portfolio_dynamics_for_24h(self, portfolio_id: int) -> PortfolioDynamicsResponse:
#         portfolio = await self.portfolio_repo.get_by_id(portfolio_id=portfolio_id)
#         if portfolio is None:
#             raise HTTPException(404, "SZ portfolio not found")
#         positions = await self.portfolio_position_repo.get_by_portfolio_id(portfolio_id=portfolio_id)
#         if not positions:
#             return PortfolioDynamicsResponse.empty(portfolio=portfolio)

#         timestamp_now = datetime.utcnow()
#         asset_ids = [pos.asset_id for pos in positions]

#         asset_prices = await self.asset_price_repo.get_prices_since(ids=asset_ids, since=timestamp_now - timedelta(days=1) )
        
#         timestamps_count = get_timestamps_count_24h(ts_now=timestamp_now)
#         time_series = get_sorted_timeseries_24h(ts_now=timestamp_now, count=timestamps_count)
#         asset_id_to_quantity = {}
#         for pos in positions:
#             asset_id_to_quantity[pos.asset_id] = pos.quantity
#         data = []
#         for ts in time_series:
#             data.append(PortfolioPrice(timestamp=ts, total_value=get_portfolio_price_by_ts(ts, asset_prices, asset_id_to_quantity)))
        
#         return PortfolioDynamicsResponse(
#             portfolio_id=portfolio.id,
#             name=portfolio.name,
#             data=data
#         )