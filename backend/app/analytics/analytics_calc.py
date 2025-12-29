from collections import deque
from datetime import datetime, timedelta
from app.analytics.models import PortfolioPositionPrepared, Lot, TradeDTO, SectorPosition, DynamicsPosition, TimeSerie

def build_only_buy_positions(trades: list[TradeDTO], current_prices, assets) -> list[PortfolioPositionPrepared]:
    id_to_lot = {}
    for t in trades:

        if t.asset_id not in id_to_lot :
            id_to_lot[t.asset_id] = deque()
        if t.direction == "buy":
            id_to_lot[t.asset_id].append({"qty" : t.quantity, "price": t.price})
        elif t.direction == "sell":
            left_to_sell = t.quantity
            
            while left_to_sell != 0:
                left_in_lot = id_to_lot[t.asset_id][0]["qty"]
                if left_in_lot > left_to_sell:
                    left_in_lot -= left_to_sell
                    left_to_sell = 0
                    id_to_lot[t.asset_id][0]["qty"] = left_in_lot
                elif left_in_lot < left_to_sell:
                    left_to_sell -= left_in_lot
                    id_to_lot[t.asset_id].popleft()
                else: 
                    left_to_sell -= left_in_lot
                    id_to_lot[t.asset_id].popleft()
    id_to_lot = {k : v for k, v in id_to_lot.items() if v}

    id_to_asset = {asset.id : asset for asset in assets}

    positive_assets = []
    for asset_id, lots in id_to_lot.items():
        asset_lots = deque()
        for lot in lots:
            asset_lots.append(Lot(qty=lot["qty"], price=lot["price"]))
        positive_assets.append(PortfolioPositionPrepared(asset_id=asset_id, lots=asset_lots, asset_market_price=current_prices[asset_id], ticker=id_to_asset[asset_id].ticker, name=id_to_asset[asset_id].full_name, sector=id_to_asset[asset_id].sector))

    return positive_assets

# PORTFOLIO SNAPSHOT

def calc_unrealized_pnl(asset_positive_positons) -> float:
    absolute_profit = 0
    for pos in asset_positive_positons:
        ap = pos.market_price - pos.mid_price * pos.quantity
        absolute_profit += ap
    return absolute_profit

def calc_cost_basis(asset_positive_positons) -> float:
    total_cost_basis = 0
    for trade in asset_positive_positons:
        total_cost_basis += trade.cost_basis
    return total_cost_basis

def calc_market_value(asset_positive_positons):
    current_value = 0
    for pos in asset_positive_positons:
        current_value += pos.market_price
    return current_value

def calc_unrealized_return_pct(unrealized_pnl: float, cost_basis: float):
    return (unrealized_pnl / cost_basis) * 100


# SECTOR DISTRIBUTION

def build_sector_positions(trades: list[TradeDTO], current_prices, assets) -> list[SectorPosition]:
    portfolio_positions = build_only_buy_positions(trades=trades, current_prices=current_prices, assets=assets)
    sector_to_pos = {}
    for pos in portfolio_positions:
        if pos.sector not in sector_to_pos:
            sector_to_pos[pos.sector] = SectorPosition(sector=pos.sector, market_value=0)
        
        sector_to_pos[pos.sector].market_value = pos.market_price
    
    return sector_to_pos.values()


def build_dynamics_positions(trades: list[TradeDTO]):
    id_to_pos = dict()

    for trade in trades:
        if trade.asset_id not in id_to_pos: id_to_pos[trade.asset_id] = DynamicsPosition(asset_id=trade.asset_id, quantity=0)
        if trade.direction == "buy":
            id_to_pos[trade.asset_id].quantity += trade.quantity
        elif trade.direction == "sell":
            id_to_pos[trade.asset_id].quantity -= trade.quantity

    return [p for i, p in id_to_pos.items() if p.quantity ]

    
def get_timestamps_count_24h(ts_now: datetime, interval_mins: int) -> int:
    ts_from = ts_now - timedelta(days=1)
    count = int ((ts_now - ts_from).total_seconds() / 60 / interval_mins)
    return count

def get_sorted_timeseries_24h(ts_now: datetime, count: int, interval_mins: int):
    time_series = []
    for i in range(count):
        ts = (ts_now - timedelta(minutes=interval_mins*i)).replace(second=0, microsecond=0)
        time_series.append(ts)
    time_series = sorted(time_series, reverse=False)
    return time_series

def build_time_series(timestamp_now, asset_prices, dynamic_positions):
    timestamps_count = get_timestamps_count_24h(ts_now=timestamp_now, interval_mins=15)
    time_series = get_sorted_timeseries_24h(ts_now=timestamp_now, count=timestamps_count, interval_mins=15)
    asset_id_to_quantity = {pos.asset_id : pos.quantity for pos in dynamic_positions}
    data = []
    for ts in time_series:
        total_price = int()
        for asset_price in asset_prices:
            timestamp = asset_price.timestamp.replace(second=0, microsecond=0)
            if timestamp == ts:
                total_price += asset_price.price * asset_id_to_quantity[asset_price.asset_id]
        data.append(TimeSerie(timestamp=ts, price=total_price))
    return data
        