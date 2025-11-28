from datetime import datetime, timedelta
from shared.repositories.asset_price import AssetPriceRepository
from shared.repositories.portfolio import PortfolioRepository
from shared.repositories.portfolio_position import PortfolioPositionRepository
class AnalyticsService:

    @staticmethod
    async def portfolio_dynamics(session, user_id: int):
        portfolios = await PortfolioRepository.get_by_user_id(session=session, user_id=user_id)
        since = datetime.utcnow() - timedelta(hours=24)
        response = []
        for portfolio in portfolios:
            positions = await PortfolioPositionRepository.get_by_portfolio_id(session=session, portfolio_id=portfolio.id)
            if not positions:
                response.append({"id": portfolio.id, "name": portfolio.name, "data": []})
                continue

            asset_ids = [p.asset_id for p in positions]
            pos_dict = {p.asset_id: p.quantity for p in positions}

            prices = await AssetPriceRepository.get_prices_since(session=session, ids=asset_ids, since=since)

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


