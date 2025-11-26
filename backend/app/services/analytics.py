

from sqlalchemy import select, func
from datetime import datetime, timedelta
from backend.app.models.portfolio import Portfolio
from backend.app.models.asset_price import AssetPrice
from backend.app.models.portfolio_position import PortfolioPosition

class AnalyticsService:

    @staticmethod
    async def portfolio_dynamics(session, user_id: int):
        q1 = select(Portfolio).where(Portfolio.user_id == user_id)
        portfolios = (await session.execute(q1)).scalars().all()
        
        portfolios_list = []
        for portfolio in portfolios:

            q2 = select(PortfolioPosition).where(
                PortfolioPosition.portfolio_id == portfolio.id
            )
            positions = (await session.execute(q2)).scalars().all()

            asset_ids = [p.asset_id for p in positions]
            pos_dict = {p.asset_id: p.quantity for p in positions}

            since = datetime.utcnow() - timedelta(hours=24)
            q3 = select(AssetPrice).where(
                AssetPrice.asset_id.in_(asset_ids),
                AssetPrice.timestamp >= since
            ).order_by(AssetPrice.timestamp)

            prices = (await session.execute(q3)).scalars().all()

            time_map = {}

            for price in prices:
                ts = price.timestamp
                asset_id = price.asset_id

                if ts not in time_map:
                    time_map[ts] = 0

                time_map[ts] += price.price * pos_dict[asset_id]
            portfolio_dict = {}
            portfolio_dict["name"] = portfolio.name
            portfolio_dict["id"] = portfolio.id
            
            ls = []
            ls = [
                    {
                        "timestamp": ts.isoformat(),
                        "value": float(val)
                    }
                    for ts, val in sorted(time_map.items(), key=lambda x: x[0])
                ]
            
            portfolio_dict["data"] = ls
            portfolios_list.append(portfolio_dict)
            

        return portfolios_list


