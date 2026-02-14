'''
https://programmingappliedai.substack.com/p/llddesign-stock-broker-platform-like
1. Core Requirements (LLD Scope)
Functional
Users can:
- Buy / Sell stocks
- View account balance
- View portfolio (holdings)

System:
- Maintains stock prices
- Matches and executes orders
- Closes open orders when stock price changes
e.g., LIMIT orders becoming executable

Non-Functional (implicitly handled in design)
- Thread safety
- Extensibility (order types, exchanges)
- Separation of concerns
'''

from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread, Lock
from uuid import uuid4
from datetime import datetime

class OrderType(Enum):
    MARKET = 1
    LIMIT = 2
                

class OrderStatus(Enum):
    OPEN = 1
    EXECUTED = 2
    CANCELLED = 3

class OrderSide(Enum):
    BUY = 1
    SELL = 2

class User:
    def __init__(self, user_id: str, balance: float):
        self.user_id = user_id
        self.account = Account(balance)
        
class PriceObserver(ABC):
    @abstractmethod
    def on_price_update(self, stock):
        pass

class Stock():
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self._observers = []
        self.lock = Lock()

    def update_price(self, price):
        with self.lock:
            self.price = price
            self.notifyObserver()

    def attach(self, observer: PriceObserver):
        self._observers.append(observer)

    def notifyObserver(self):
        for observer in self._observers:
            observer.on_price_update(self)

class Order(PriceObserver):
    def __init__(self, user: User, stock: Stock, quantity: int, orderType: OrderType, side: OrderSide, limit_price: float):
        self.order_id = uuid4()
        self.user = user
        self.stock = stock
        self.quantity = quantity
        self.orderType = orderType
        self.side = side
        self.limit_price = limit_price
        self.status = OrderStatus.OPEN
        self.created_at = datetime.now()

    @abstractmethod
    def is_executable(self, market_price):
        pass

    def execute(self, execution_price):
        self.status = OrderStatus.EXECUTED
        self.user.account.apply_trade(self.stock, self.quantity, self.side, execution_price)

    def on_price_update(self, stock: Stock):
        pass


class BuyOrder(Order):
    def __init__(self, user: User, stock: Stock, quantity: int, type: OrderType, limit_price: float):
        super().__init__(user, stock, quantity, type, OrderSide.BUY, limit_price)

    def is_executable(self, market_price):
        if self.orderType == OrderType.MARKET:
            return True
        return market_price <= self.limit_price
    
    def on_price_update(self, stock: Stock):
        if self.status == OrderStatus.OPEN and self.is_executable(stock.price):
            self.execute(stock.price)


class SellOrder(Order):
    def __init__(self, user: User, stock: Stock, quantity: int, type: OrderType, limit_price: float):
        super().__init__(user, stock, quantity, type, OrderSide.SELL, limit_price)

    def is_executable(self, market_price):
        if self.orderType == OrderType.MARKET:
            return True
        return market_price >= self.limit_price
    
    def on_price_update(self, stock: Stock):
        if self.status == OrderStatus.OPEN and self.is_executable(stock.price):
            self.execute(stock.price)

class Account:
    def __init__(self, balance: float):
        self.balance = balance
        self.portfolio = Portfolio()
        self.lock = Lock()

    def apply_trade(self, stock: Stock, quantity: int, side: OrderSide, price: float):
        with self.lock:
            amount = quantity * price
            if side == OrderSide.BUY:
                self.balance -= amount
                self.portfolio.addStock(stock, quantity)
            else:
                self.balance += amount
                self.portfolio.removeStock(stock, quantity)

class Portfolio:
    def __init__(self):
        self.holdings = {}

    def addStock(self, stock: Stock, quantity: int):
        self.holdings[stock.symbol] = self.holdings.get(stock.symbol, 0) + quantity

    def removeStock(self, stock: Stock, quantity: int):
        self.holdings[stock.symbol] = self.holdings.get(stock.symbol, 0) - quantity

class OrderService:  
    def placeOrder(self, order: Order):
        order.stock.attach(order)
        if order.orderType == OrderType.MARKET:
            order.execute(order.stock.price)

class StockBrokerApp:

    def test(self):
        tcs = Stock("TCS", 3500.0)
        user = User("user-1", 100000.0)
        orderService = OrderService()
        buyOrder = BuyOrder(user, tcs, 10, OrderType.LIMIT, 3400.0)
        orderService.placeOrder(buyOrder)
        print(f"Order placed. Current status: {buyOrder.status}")

        print(f"Updating price to 3450...")
        tcs.update_price(3450.0)
        print(f"Order Status: {buyOrder.status}")

        print(f"Updating price to 3399...")
        tcs.update_price(3390.0)
        print(f"Order Status: {buyOrder.status}")


broker = StockBrokerApp()
broker.test()