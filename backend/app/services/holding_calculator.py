from typing import List, Dict
from app.models.transaction import Transaction
from app.schemas.holding import Holding
from app.schemas.transaction import TransactionType

class BuyBatch:
    def __init__(self, quantity: float, price: float):
        self.quantity = float(quantity)
        self.price = float(price)

def calculate_holdings(transactions: List[Transaction]) -> List[Holding]:
    # Group by symbol
    grouped_txs: Dict[str, List[Transaction]] = {}
    
    # Pre-sort transactions by date just in case
    sorted_txs = sorted(transactions, key=lambda x: (x.trade_date, x.created_at if hasattr(x, 'created_at') else ''))

    for tx in sorted_txs:
        if tx.symbol not in grouped_txs:
            grouped_txs[tx.symbol] = []
        grouped_txs[tx.symbol].append(tx)
    
    holdings = []
    
    for symbol, txs in grouped_txs.items():
        batches: List[BuyBatch] = []
        realized_profit = 0.0
        
        market = txs[0].market if txs else "KR" # Assume market doesn't change for symbol
        
        for tx in txs:
            qty = float(tx.quantity)
            price = float(tx.price)
            
            if tx.type == TransactionType.BUY:
                batches.append(BuyBatch(qty, price))
            elif tx.type == TransactionType.SELL:
                qty_to_sell = qty
                
                while qty_to_sell > 0 and batches:
                    current_batch = batches[0]
                    
                    if current_batch.quantity > qty_to_sell:
                        # Partial sell from this batch
                        profit = (price - current_batch.price) * qty_to_sell
                        realized_profit += profit
                        current_batch.quantity -= qty_to_sell
                        qty_to_sell = 0
                    else:
                        # Full sell of this batch
                        sell_amount = current_batch.quantity
                        profit = (price - current_batch.price) * sell_amount
                        realized_profit += profit
                        qty_to_sell -= sell_amount
                        batches.pop(0) # Remove empty batch
                        
                # Handle oversell? (Should be validated before, but for calc just ignore or negative?)
                # If batches empty but still need to sell, we can't calc profit correctly (cost basis missing).
                # Assume validation ensures valid sell.
                
        # Calculate final holding stats from remaining batches
        total_qty = sum(b.quantity for b in batches)
        
        if total_qty > 0:
            total_cost = sum(b.quantity * b.price for b in batches)
            avg_price = total_cost / total_qty
            
            holdings.append(Holding(
                symbol=symbol,
                market=market,
                quantity=total_qty,
                avg_price=avg_price,
                total_realized_profit=realized_profit
            ))
        elif realized_profit != 0:
             # Holdings sold out, but keep record? Usually "Asset Status" shows current assets.
             # If quantity is 0, we generally don't show it in "Holdings" list, 
             # but maybe "Realized Gain" report needs it.
             # T3.1 asks for "Current Status". If 0, don't return.
             pass
             
    return holdings
