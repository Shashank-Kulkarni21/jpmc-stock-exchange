from abc import ABC, abstractmethod
from collections import deque

# Abstract Stock Class
class Stock(ABC):
    def __init__(self, symbol, stock_type, last_dividend, par_value, fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type  # "Common" or "Preferred"
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = deque()  # Stores trades (timestamp, quantity, buy/sell, price)


    @abstractmethod
    def calculate_dividend_yield(self, price):
        pass

# Concrete Stock Classes
class CommonStock(Stock):
    def calculate_dividend_yield(self, price):
        return self.last_dividend / price if price > 0 else 0

class PreferredStock(Stock):
    def __init__(self, symbol, stock_type, last_dividend, par_value, fixed_dividend):
        super().__init__(symbol, stock_type, last_dividend, par_value, fixed_dividend)
        self.fixed_dividend = fixed_dividend

    def calculate_dividend_yield(self, price):
        return (self.fixed_dividend * self.par_value) / price if price > 0 else 0

# Factory Class
class StockFactory:
    @staticmethod
    def create_stock(symbol, stock_type, last_dividend, par_value, fixed_dividend=None):
        if stock_type == "Common":
            return CommonStock(symbol, stock_type, last_dividend, par_value, fixed_dividend)
        elif stock_type == "Preferred":
            return PreferredStock(symbol, stock_type, last_dividend, par_value, fixed_dividend)
        else:
            raise ValueError("Invalid stock type")
