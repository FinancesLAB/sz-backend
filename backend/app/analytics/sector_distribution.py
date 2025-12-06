from typing import List, Dict
from shared.models.portfolio_position import PortfolioPosition

def calc_portfolio_current_value(positions: List[PortfolioPosition], current_prices: Dict[int, float]) -> int:
    total_value=0
    for position in positions:
        total_value+=position.quantity * current_prices[position.asset_id]
    return total_value

def calc_position_current_value(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
    return position.quantity * current_prices[position.asset_id]
