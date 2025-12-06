from datetime import datetime, timedelta
from typing import Dict

def get_timestamps_count_24h(ts_now: datetime) -> int:
    ts_from = ts_now - timedelta(days=1)
    count = int ((ts_now - ts_from).total_seconds() / 60 / 15)
    return count

def get_sorted_timeseries_24h(ts_now: datetime, count: int):
    time_series = []
    for i in range(count):
        ts = (ts_now - timedelta(minutes=15*i)).replace(second=0, microsecond=0)
        time_series.append(ts)
    time_series = sorted(time_series, reverse=False)
    return time_series

def get_portfolio_price_by_ts(ts, asset_prices, id_to_q: Dict[int, int]) -> float:
    total_price = 0
    for asset_price in asset_prices:
        timestamp = asset_price.timestamp.replace(second=0, microsecond=0)
        if timestamp == ts:
            total_price += asset_price.price * id_to_q[asset_price.asset_id]
    return total_price if total_price != 0 else 0