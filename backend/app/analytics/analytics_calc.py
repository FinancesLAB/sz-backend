from collections import deque
from typing import List

from app.analytics.models import AssetPosition, Lot, TradeDTO

def build_only_buy_positions(trades: List[TradeDTO], current_prices) -> List[AssetPosition]:
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
    positive_assets = []
    for asset_id, lots in id_to_lot.items():
        asset_lots = deque()
        for lot in lots:
            asset_lots.append(Lot(qty=lot["qty"], price=lot["price"]))
        positive_assets.append(AssetPosition(asset_id=asset_id, lots=asset_lots, asset_market_price=current_prices[asset_id]))

    return positive_assets


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
    # self.upnl / self.cb * 100
    return (unrealized_pnl / cost_basis) * 100
