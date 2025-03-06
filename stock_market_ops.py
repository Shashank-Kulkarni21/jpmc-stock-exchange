import time
import math
import logging
import asyncio
from datetime import datetime, timedelta
from collections import deque
from stock_factory import StockFactory, Stock

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class StockOps:
    """
    Represents a stock in the Global Beverage Corporation Exchange.
    Supports async dividend calculations and trade recording.
    """
    def __init__(self):
        pass

    async def calculate_dividend_yield(self, price):
        """Asynchronously calculates the dividend yield."""
        await asyncio.sleep(0)  # Simulating async execution
        try:
            if price <= 0:
                raise ValueError("Price must be greater than zero")

            if self.stock_type == "Common":
                return self.last_dividend / price
            elif self.stock_type == "Preferred" and self.fixed_dividend is not None:
                return (self.fixed_dividend * self.par_value) / price
            else:
                raise ValueError(f"Invalid stock type: {self.stock_type}")
        except Exception as e:
            logging.error(f"Error calculating dividend yield for {self.symbol}: {e}")
            return None

    async def calculate_pe_ratio(self, price, stock):
        """Asynchronously calculates the P/E Ratio."""
        await asyncio.sleep(0)
        try:
            if stock.last_dividend == 0:
                logging.warning(f"Dividend is zero for {stock.symbol}, P/E Ratio is infinite.")
                return float('inf')  # Infinite P/E Ratio when dividend is zero
            return price / stock.last_dividend
        except Exception as e:
            logging.error(f"Error calculating P/E ratio for {stock.symbol}: {e}")
            return None

    async def record_trade(self, stock, quantity, trade_type, price):
        """Records a trade with timestamp, quantity, trade type (BUY/SELL), and price."""
        await asyncio.sleep(0)
        try:
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be greater than zero")
            if trade_type not in ["BUY", "SELL"]:
                raise ValueError("Trade type must be BUY or SELL")

            timestamp = datetime.now()
            stock.trades.append((timestamp, quantity, trade_type, price))
            logging.info(f"Trade recorded for {stock.symbol}: {trade_type} {quantity} at {price}")

        except Exception as e:
            logging.error(f"Error recording trade for {stock.symbol}: {e}")

    async def calculate_volume_weighted_stock_price(self, stock):
        """Asynchronously calculates the Volume Weighted Stock Price based on trades in the last 5 minutes."""
        await asyncio.sleep(0)
        try:
            now = datetime.now()
            past_five_minutes = now - timedelta(minutes=5)
            relevant_trades = [(qty, price) for ts, qty, _, price in stock.trades if ts >= past_five_minutes]

            if not relevant_trades:
                logging.warning(f"No trades in the last 5 minutes for {stock.symbol}. Returning 0.")
                return 0  # No trades in the last 5 minutes

            total_price_qty = sum(qty * price for qty, price in relevant_trades)
            total_qty = sum(qty for qty, _ in relevant_trades)
            return total_price_qty / total_qty if total_qty else 0
        except Exception as e:
            logging.error(f"Error calculating VWSP for {stock.symbol}: {e}")
            return None

class StockMarket:
    """
    Represents the Global Beverage Corporation Exchange (GBCE).
    Manages multiple stocks and calculates the All Share Index asynchronously.
    """
    def __init__(self):
        self.stocks = {}
        self.stock_ops = StockOps()
        

    async def add_stock(self, stock):
        """Registers a stock asynchronously."""
        await asyncio.sleep(0)
        try:
            if not isinstance(stock, Stock):
                raise TypeError("Only Stock objects can be added.")
            self.stocks[stock.symbol] = stock
            logging.info(f"Stock {stock.symbol} added to the market.")
        except Exception as e:
            logging.error(f"Error adding stock: {e}")

    async def get_all_share_index(self):
        """Calculates the GBCE All Share Index using the geometric mean of all VWSP values asynchronously."""
        try:
            prices = await asyncio.gather(
                *[self.stock_ops.calculate_volume_weighted_stock_price(stock) for stock in self.stocks.values()]
            )
            prices = [p for p in prices if p and p > 0]

            if not prices:
                logging.warning("No valid stock prices available to calculate GBCE All Share Index. Returning 0.")
                return 0  # No valid stock prices to calculate mean

            product = math.prod(prices)
            return product ** (1 / len(prices))
        except Exception as e:
            logging.error(f"Error calculating GBCE All Share Index: {e}")
            return None

async def main():
    # Sample Stocks
    stocks = [
        StockFactory.create_stock("TEA", "Common", 0, 100),
        StockFactory.create_stock("POP", "Common", 8, 100),
        StockFactory.create_stock("ALE", "Common", 23, 60),
        StockFactory.create_stock("GIN", "Preferred", 8, 100, 0.02),
        StockFactory.create_stock("JOE", "Common", 13, 250)
    ]
    stock_ops = StockOps()
    # Initialize Stock Market
    market = StockMarket()
    await asyncio.gather(*(market.add_stock(stock) for stock in stocks))

    # Simulating Trades
    await asyncio.gather(
        # market.stocks["POP"].record_trade(quantity=100, trade_type="BUY", price=120),
        # .record_trade(quantity=50, trade_type="SELL", price=125),
        # market.stocks["GIN"].record_trade(quantity=200, trade_type="BUY", price=150),
        stock_ops.record_trade(market.stocks["POP"], quantity=200, trade_type="BUY", price=150),
        stock_ops.record_trade(market.stocks["POP"], quantity=50, trade_type="SELL", price=125),
        stock_ops.record_trade(market.stocks["GIN"], quantity=200, trade_type="BUY", price=150)
        
    )

    # Calculating stock statistics concurrently
    logging.info("Stock Calculations:")
    for symbol, stock in market.stocks.items():
        try:
            price = 100  # Example price input
            dividend_yield = stock.calculate_dividend_yield(price),
            pe_ratio, vwsp = await asyncio.gather(
                stock_ops.calculate_pe_ratio(price, stock),
                stock_ops.calculate_volume_weighted_stock_price(stock)
            )

            logging.info(f"\nStock: {symbol}")
            logging.info(f"Dividend Yield: {dividend_yield}" if dividend_yield is not None else "N/A")
            logging.info(f"P/E Ratio: {pe_ratio:.2f}" if pe_ratio is not None else "N/A")
            logging.info(f"Volume Weighted Stock Price: {vwsp:.2f}" if vwsp is not None else "N/A")

        except Exception as e:
            logging.error(f"Error processing {symbol}: {e}")

    gbce_index = await market.get_all_share_index()
    logging.info(f"\nGBCE All Share Index: {round(gbce_index, 2)}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
