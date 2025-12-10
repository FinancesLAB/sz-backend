
from typing import List, Dict
from shared.models.trade import Trade
from collections import deque
# def calc_portfolio_current_value(positions: List[PortfolioPosition], current_prices: Dict[int, float]) -> float:
#     total_value=0
#     for position in positions:
#         total_value+=position.quantity * current_prices[position.asset_id]
#     return total_value

# def calc_position_current_value(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
#     return position.quantity * current_prices[position.asset_id]

# def calc_invested_value(positions: List[PortfolioPosition]) -> float:
#     total_invested_value=0
#     for position in positions:
#         total_invested_value+=position.quantity * position.avg_price
#     return total_invested_value

# def calc_profit(current_value: int, invested_value: int) -> float:
#     return current_value - invested_value

# def calc_position_profit_percent(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
#     return ((current_prices[position.asset_id] - position.avg_price) / position.avg_price) * 100

# def calc_position_profit(position: PortfolioPosition, current_prices: Dict[int, float]) -> float:
#     return position.quantity * current_prices[position.asset_id] - position.quantity * position.avg_price

# def calc_portfolio_profit_percent(profit: int, invested_value: int) -> float:
#     return profit / invested_value * 100

# def calc_position_weight_in_portfolio(position: PortfolioPosition, current_prices: Dict[int, float], total_value: float) -> float:
#     return ((position.quantity * current_prices[position.asset_id]) / total_value) * 100

def get_portfolio_purchase_price(portfolio_trades: List[Trade]):
    total = 0
    for trade in portfolio_trades:
        if trade.direction == "buy":
            total += trade.price * trade.quantity
        elif trade.direction == "sell":
            total -= trade.price * trade.quantity
    return total

# def get_portfolio_positions_count(portfolio_trades: List[Trade]):
    
def get_asset_id_to_quantity_dict(portfolio_trades: List[Trade]):
    asset_id_to_quantity = dict()
    for trade in portfolio_trades:
        asset_id_to_quantity[trade.asset_id] = asset_id_to_quantity.get(trade.asset_id, 0)
        if trade.direction == "buy": asset_id_to_quantity[trade.asset_id] += trade.quantity
        elif trade.direction == "sell": asset_id_to_quantity[trade.asset_id] -= trade.quantity
    return asset_id_to_quantity


def calc_unrealized_pnl(portfolio_trades: List[Trade], asset_prices: Dict[int, float]): #portfolio_trades sort asc
    id_to_lot = dict() # {asset_id: deque(qty: price, qty: price)} - онли покупки а вычитаем только если встречаем продажу
    
    for t in portfolio_trades:
        if t.asset_id not in id_to_lot:
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
    mid_prices = {}
    quantities = {}
    for a_id, lots in id_to_lot.items():
        mid_prices[a_id] = sum([(lot["qty"] * lot["price"]) for lot in lots]) / sum([lot["qty"] for lot in lots])
        quantities[a_id] = sum(lot["qty"] for lot in lots)
    
    absolute_profit = sum(asset_prices[a_id] * quantities[a_id] - mid_prices[a_id] * quantities[a_id] for a_id in id_to_lot.keys())
    print(id_to_lot)
    return absolute_profit