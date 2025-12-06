from shared.models.portfolio_position import PortfolioPosition
from typing import List, Dict

def calc_portfolio_current_value(positions: List[PortfolioPosition], current_prices: Dict[int, float]) -> float:
    total_value=0
    for position in positions:
        total_value+=position.quantity * current_prices[position.asset_id]
    return total_value

def calc_position_current_value(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
    return position.quantity * current_prices[position.asset_id]

def calc_invested_value(positions: List[PortfolioPosition]) -> float:
    total_invested_value=0
    for position in positions:
        total_invested_value+=position.quantity * position.avg_price
    return total_invested_value

def calc_profit(current_value: int, invested_value: int) -> float:
    return current_value - invested_value

def calc_position_profit_percent(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
    return ((current_prices[position.asset_id] - position.avg_price) / position.avg_price) * 100

def calc_position_profit(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
    return position.quantity * current_prices[position.asset_id] - position.quantity * position.avg_price

def calc_portfolio_profit_percent(profit: int, invested_value: int) -> float:
    return profit / invested_value * 100

def calc_position_weight_in_portfolio(position: PortfolioPosition, current_prices: Dict[int, float], total_value: float) -> float:
    return ((position.quantity * current_prices[position.asset_id]) / total_value) * 100
