#Singleton pattern
# Interview Question: "Design a configuration manager that should have only one instance throughout the application."

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self, db_name):
        if not self.connection:
            self.connection = f"Connected to {db_name}"
            print(self.connection)

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def log(self, message):
        print(f"[LOG]: {message}")


# logger1 = Logger()
# logger2 = Logger()
# print(logger1 is logger2)
# logger1.log("Hello")

    
# Factory Pattern
# Creates objects without specifying exact class
from abc import ABC, abstractmethod

class Vehicle:
    @abstractmethod
    def create(self):
        pass

class Car(Vehicle):
    def create(self):
        return "Car created"

class Bike(Vehicle):
    def create(self):
        return "Bike created"

class VehicleFactory:
    @staticmethod
    def get_vehicle(vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "bike":
            return Bike()
        return None
    
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via PayPal"

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via Stripe"
    
class PaymentFactory:
    @staticmethod
    def create_processor(method):
        processors = {
            'paypal': PayPalProcessor,
            'stripe': StripeProcessor
        }
        return processors.get(method, PayPalProcessor)()
    
processor = PaymentFactory.create_processor('stripe')
print(processor.process_payment(100))

# Interview Question: "Design a notification system that can send emails, SMS, or push notifications based on user preference."
class Notification(ABC):
    @abstractmethod
    def notify(self, message):
        pass

class Email(Notification):
    def notify(self, message):
        return f"[Email]: {message} sent"
class Sms(Notification):
    def notify(self, message):
        return f"[SMS]: {message} sent"
class Push(Notification):
    def notify(self, message):
        return f"[Push]: {message} sent"
    
class NotificationFactory:
    @staticmethod
    def create(method):
        processor = {
            'email': Email,
            'sms': Sms,
            'push': Push
        }
        return processor.get(method, Email)()
    
n = NotificationFactory.create('email')
print(n.notify("Hello world"))

# 3. Builder Pattern
# Constructs complex objects step by step

class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni  = False
        self.corn = False
        
    def __str__(self):
        return f"Pizza: size={self.size}, cheese={self.cheese}, pepperoni={self.pepperoni}, corn={self.corn}"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self
    
    def add_cheese(self):
        self.pizza.cheese = True
        return self

    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self
    
    def add_corn(self):
        self.pizza.corn = True
        return self
    
    def build(self):
        return self.pizza
    
pizza = PizzaBuilder().set_size("Medium").add_cheese().add_corn().build()
print(pizza)

class SQLQueryBuilder:
    def __init__(self):
        self.query_parts = {}

    def select(self, fields):
        self.query_parts['select'] = f"SELECT {', '.join(fields)}"
        return self
    
    def from_table(self, table):
        self.query_parts['from'] = f"FROM {table}"
        return self
    
    def where(self, condition):
        self.query_parts['where'] = f"WHERE {condition}"
        return self
    
    def build(self):
        order = ['select', 'from', 'where']
        return ' '.join(self.query_parts.get(key, '') for key in order if key in self.query_parts)
    
query = SQLQueryBuilder().select(['name', 'email']).from_table('users').where('age > 18').build()

print(query)

# Interview Question: "Design an HTTP request builder that allows setting headers, query parameters, and body."
## ToDo

# 4. Prototype Pattern
# Clones objects instead of creating new ones

import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)
    
class Document(Prototype):
    def __init__(self, title, content, formatting):
        self.title = title
        self.content = content
        self.formatting = formatting

    def __str__(self):
        return f"Document: {self.title}, Content: {self.content}..."
    
template = Document("Temp", "Hare Krishma..", {"font":"Arial", "size": 12})
doc1 = template.clone()
doc1.title = "Report 1"
doc1.content = "Hari bol..."
doc2 = template.clone()
doc2.title = "Report 2"

print(template)
print(doc1)
print(doc2)

# Interview Question: "Design a system where game characters can be cloned with their current state."

# Structural Patterns
# 5. Adapter Pattern
# Makes incompatible interfaces work together

class OldPaymentSystem:
    def make_payment(self, amount):
        return f"Old system: paid {amount}"

class NewPaymentInterface:
    def process(self, amount):
        pass

class PaymentAdapter(NewPaymentInterface):
    def __init__(self, old_system):
        self.old_system = old_system

    def process(self, amount):
        return self.old_system.make_payment(amount)
    

old_system = OldPaymentSystem()
adapter = PaymentAdapter(old_system)
print(adapter.process(100))

# Interview Question: "You need to integrate a third-party analytics library with a different API into your existing tracking system."

# 6. Decorator Pattern
# Adds new functionality to objects dynamically

# Interview Example: API Endpoint with Authentication and Logging
class Component:
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "Basic Operation"
    
class Decorator(Component):
    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation()
    
class LoggingDecorator(Decorator):
    def operation(self):
        result = self._component.operation()
        print(f"[LOG]: {result}")
        return result

class AuthDecorator(Decorator):
    def operation(self):
        print(f"[AUTH]: checking authentication...")
        return self._component.operation()
        

# ex 2
#  Real-world API example
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start:.4f}s")
        return result
    return wrapper

def cache_decorator(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            print("Returning cached result")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@timing_decorator
@cache_decorator
def expensive_operation(n):
    import time
    time.sleep(1)
    return n * n

# # Usage
# print(expensive_operation(5))
# print(expensive_operation(5))  # Cached

# Interview Question: "Design a text processing system where you can add features like spell-check, grammar-check, and formatting dynamically."

# 7. Facade Pattern
# Provides a simplified interface to complex subsystems
# Interview Example: E-commerce Order Processing

class Inventory:
    def check_availability(self, product_id):
        print(f"Checking inventory for {product_id}")
        return True

class Payment:
    def process_payment(self, amount):
        print(f"Processing payment of ${amount}")
        return True

class Shipping:
    def arrange_shipping(self, address):
        print(f"Arranging shipping to {address}")
        return "TRACK123"
    
class OrderFacade:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()

    def place_order(self, product_id, amount, address):
        print("=== Starting Order Process ===")
        if not self.inventory.check_availability(product_id):
            return "Product unavailable"
        if not self.payment.process_payment(amount):
            return "Payment failed"
        
        tracking = self.shipping.arrange_shipping(address)
        print("=== Order Completed ===")
        return f"Order placed successfully. Tracking: {tracking}"
    
order_system = OrderFacade()
result = order_system.place_order("Prod123", 99.99, "123, main st")
print(result)

# Interview Question: "Design a home automation system that simplifies controlling lights, thermostat, and security system."

# 8. Proxy Pattern
# Controls access to another object
# Interview Example: Image Loading with Lazy Initialization

class Image:
    def display(self):
        pass

class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"Loading image from disk: {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageProxy(Image):
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()


image = ImageProxy("larger_photo.jpg")
print("Image object created")

image.display()
image.display()
# Interview Question: "Design a caching proxy for database queries to reduce load."


# Behavioral Patterns
# 9. Observer Pattern
# Notifies multiple objects about state changes

# Interview Example: Stock Price Monitoring System

class Subject:
    def __init__(self):
        self._obeservers = []
        self._state = None

    def attach(self, observer):
        self._obeservers.append(observer)

    def detach(self, observer):
        self._obeservers.remove(observer)

    def notify(self):
        for observer in self._obeservers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()

class Observer:
    def update(self, state):
        pass

class StockPriceMonitor(Subject):
    def __init__(self, stock_name):
        super().__init__()
        self.stock_name = stock_name

    def set_price(self, price):
        print(f"\n{self.stock_name} price changed to ${price}")
        self.set_state(price)

class EmailAlert(Observer):
    def __init__(self, email):
        self.email = email

    def update(self, price):
        print(f"Email sent to {self.email}: Price is now ${price}")

class SMSAlert(Observer):
    def __init__(self, phone):
        self.phone = phone

    def update(self, price):
        print(f"SMS sent to {self.phone}: Price is now ${price}")

stock = StockPriceMonitor("AAPL")
email_alert = EmailAlert("usr@gmail.com")
sms_alert = SMSAlert("889-234")

stock.attach(email_alert)
stock.attach(sms_alert)

stock.set_price(150.00)
stock.set_price(155.00)
# Interview Question: "Design a notification system where users can subscribe to different events in a social media application."

# 10. Strategy Pattern
# Defines a family of algorithms and makes them interchangeable
# Interview Example: Shipping Cost Calculator

class ShippingStrategy:
    def calculate(self, weight):
        pass

class StandardShipping(ShippingStrategy):
    def calculate(self, weight):
        return weight * 5

class ExpressShipping(ShippingStrategy):
    def calculate(self, weight):
        return weight * 10

class OvernightShipping(ShippingStrategy):
    def calculate(self, weight):
        return weight * 20
    
class ShippingCalculator:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def calculate_cost(self, weight):
        return self._strategy.calculate(weight)
    
calculator = ShippingCalculator(StandardShipping())
print(f"Standard: ${calculator.calculate_cost(10)}")

calculator.set_strategy(ExpressShipping())
print(f"Express: ${calculator.calculate_cost(10)}")

# Real wordstrategy
class SortStrategy:
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return QuickSort().sort(left) + middle + QuickSort().sort(right)

class MergeSort(SortStrategy):
    def sort(self, data):
        if(len(data) <= 1):
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # while i < len(left):
        #     result.append(left[i])
        #     i += 1
        # while j < len(right):
        #     result.append(right[j])
        #     j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
class Sorter:
    def __init__(self, strategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)
    
data = [64, 34, 25, 12, 22, 11, 90]
sorter = Sorter(QuickSort())
print(sorter.sort(data))

# Interview Question: "Design a payment processing system that supports multiple payment methods with different fee structures."

# 11. Command Pattern
# Encapsulates requests as objects
# Interview Example: Text Editor with Undo/Redo

class Command:
    def execuete(self):
        pass

    def undo(self):
        pass

class TextEditor:
    def __init__(self):
        self.text = ""
    
    def write(self, text):
        self.text += text

    def delete(self, length):
        self.text = self.text[:-length]

    def get_text(self):
        return self.text
    
class WriteCommand(Command):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text

    def execute(self):
        self.editor.write(self.text)

    def undo(self):
        self.editor.delete(len(self.text))

class CommandManager:
    def __init__(self):
        self.history = []
        self.current = -1

    def execute(self, command):
        self.history = self.history[:self.current + 1]
        command.execute()
        self.history.append(command)
        self.current += 1

    def undo(self):
        if self.current >= 0:
            self.history[self.current].undo()
            self.current -= 1

# Usage
editor = TextEditor()
manager = CommandManager()

manager.execute(WriteCommand(editor, "Hello "))
manager.execute(WriteCommand(editor, "World"))
print(editor.get_text())  # "Hello World"

manager.undo()
print(editor.get_text())  # "Hello "

manager.undo()
print(editor.get_text())  # ""

# Interview Question: "Design a remote control system for home devices that supports undo functionality."

# 12. Template Method Pattern
# Defines skeleton of algorithm, subclasses override steps

# Interview Example: Data Processing Pipeline

from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process(self):
        """Template Method"""
        self.read_data()
        self.process_data()
        self.validate_data()
        self.save_data()

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def process_data(self):
        pass
    
    def validate_data(self):
        print("Validating data...")
    
    @abstractmethod
    def save_data(self):
        pass   

class CSVProcessor(DataProcessor):
    def read_data(self):
        print("Reading CSV file")
    
    def process_data(self):
        print("Processing CSV data")
    
    def save_data(self):
        print("Saving to database")

class JSONProcessor(DataProcessor):
    def read_data(self):
        print("Reading JSON file")
    
    def process_data(self):
        print("Processing JSON data")
    
    def save_data(self):
        print("Saving to cloud storage")

# Usage
print("=== CSV Processing ===")
csv_processor = CSVProcessor()
csv_processor.process()

print("\n=== JSON Processing ===")
json_processor = JSONProcessor()
json_processor.process()

# Interview Question: "Design a test framework where test cases follow a standard setup-execute-teardown pattern."

# 13. State Pattern
# Changes behavior based on internal state
# Interview Example: Order State Management

# Interview Example: Order State Management
class OrderState(ABC):
    @abstractmethod
    def process(self, order):
        pass

class PendingState(OrderState):
    def process(self, order):
        print("Order is pending. Moving to confirmed.")
        order.state = ConfirmedState()

class ConfirmedState(OrderState):
    def process(self, order):
        print("Order confirmed. Processing payment.")
        order.state = ProcessingState()

class ProcessingState(OrderState):
    def process(self, order):
        print("Payment processed. Shipping order.")
        order.state = ShippedState()

class ShippedState(OrderState):
    def process(self, order):
        print("Order has been shipped. Delivering.")
        order.state = DeliveredState()

class DeliveredState(OrderState):
    def process(self, order):
        print("Order delivered. Process complete.")

class Order:
    def __init__(self):
        self.state = PendingState()
    
    def proceed(self):
        self.state.process(self)

# Usage
order = Order()
for _ in range(5):
    order.proceed()
    # print()

# Interview Question: "Design a vending machine with different states: idle, has money, dispensing, out of stock."

# 14. Chain of Responsibility Pattern
# Passes requests along a chain of handlers

# Interview Example: Support Ticket System
class Handler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None
    
class LevelL1Support(Handler):
    def handle(self, request):
        if request['priority'] == 'low':
            return f"Level 1 handled: {request['issue']}"
        return super().handle(request)

class LevelL2Support(Handler):
    def handle(self, request):
        if request['priority'] == 'medium':
            return f"Level 2 handled: {request['issue']}"
        return super().handle(request)
    
class LevelL3Support(Handler):
    def handle(self, request):
        if request['priority'] == 'high':
            return f"Level 3 handled: {request['issue']}"
        return super().handle(request)

level1 = LevelL1Support()
level2 = LevelL2Support()
level3 = LevelL3Support()

level1.set_next(level2).set_next(level3)

requests = [
    {'issue': 'Password reset', 'priority': 'low'},
    {'issue': 'Database error', 'priority': 'medium'},
    {'issue': 'System crash', 'priority': 'high'}
]

for req in requests:
    result = level1.handle(req)
    print(result)

# Interview Question: "Design a logging system where log messages pass through filters for severity levels."

# 15. Iterator Pattern
# Traverses elements without exposing structure

# Interview Example: Custom Collection Iterator
class Book:
    def __init__(self, title):
        self.title = title

class BookCollection:
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def __iter__(self):
        return BoolIterator(self._books)
    
class BoolIterator:
    def __init__(self, books):
        self._books = books
        self._index = 0

    def __next__(self):
        if self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            return book
        raise StopIteration
    
# Usage
collection = BookCollection()
collection.add_book(Book("Design Patterns"))
collection.add_book(Book("Clean Code"))
collection.add_book(Book("Refactoring"))

for book in collection:
    print(book.title)

# Python's built-in iterator
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

# Usage
rev = ReverseIterator([1, 2, 3, 4, 5])
for num in rev:
    print(num, end=' ')

# Interview Question: "Design a pagination system for traversing large datasets."
