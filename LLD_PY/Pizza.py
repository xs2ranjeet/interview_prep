'''
https://substack.com/inbox/post/181400819
LLD: Design Pizza Pricing System

Functional Requirements
1. Pizza Creation
    - User can choose pizza size: SMALL, MEDIUM, LARGE
    - Base price depends on size.

2. Add-ons / Toppings
    - Toppings: Corn, Onion, CheeseBurst, etc.
    - Each topping has:
        Price per serving
        Rules (constraints/discounts)

3. Business Rules
    - Cheese Burst cannot be added to SMALL pizza.
    - Corn has 30% discount if servings > 2.

4. Final Price Calculation
    - Provide a function to compute the final price.
'''
from enum import Enum
from typing import defaultdict
from abc import ABC, abstractmethod

class PizzaSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class ToppingType(Enum):
    CORN = 1
    ONION = 2
    CHEESE_BURST = 3

pizzaPrice = {PizzaSize.SMALL: 100, PizzaSize.MEDIUM: 150, PizzaSize.LARGE: 200}

class Pizza:
    def __init__(self, size: PizzaSize, toppings: dict):
        self.size = size
        self.base_price = pizzaPrice[size]
        self.toppings = toppings

    def add_toppings(self, topping: ToppingType, serving: int):
        self.toppings[topping] += serving

class Topping(ABC):
    @abstractmethod
    def price_per_serving(self) -> float:
        pass

class CornTopping(Topping):
    def price_per_serving(self) -> float:
        return 30
    
class OnionTopping(Topping):
    def price_per_serving(self) -> float:
        return 20

class CheeseBurstTopping(Topping):
    def price_per_serving(self) -> float:
        return 50

class ToppingFactory:

    @staticmethod
    def create(topping_type: ToppingType):
        return {
            ToppingType.CORN: CornTopping(),
            ToppingType.ONION: OnionTopping(),
            ToppingType.CHEESE_BURST:CheeseBurstTopping()
        }[topping_type]

class PricingRule(ABC):
    @abstractmethod
    def is_applicable(self, pizza: Pizza) -> bool:
        pass

    @abstractmethod
    def apply(self, pizza: Pizza, currentPrice: float) -> float:
        pass

class CornBulkDiscountRule(PricingRule):
    def is_applicable(self, pizza: Pizza) -> bool:
        return pizza.toppings.get(ToppingType.CORN, 0) > 2

    def apply(self, pizza: Pizza, price: float) -> float:
        corn_units = pizza.toppings[ToppingType.CORN]
        discount = corn_units * 30 * 0.3
        return price - discount

class CheeseCornComboRule(PricingRule):
    def is_applicable(self, pizza: Pizza) -> bool:
        return (
            ToppingType.CORN in pizza.toppings
            and ToppingType.CHEESE_BURST in pizza.toppings
            and pizza.size != PizzaSize.SMALL
        )
        
    def apply(self, pizza: Pizza, price: float) -> float:
        return price - 20   

class PriceRuleEngine:

    rules = [CornBulkDiscountRule(), CheeseCornComboRule()]

    @classmethod
    def apply(cls, pizza: Pizza, price: float) -> float :
        for rule in cls.rules:
            if rule.is_applicable(pizza) :
                price = rule.apply(pizza, price)
        return price

class PriceCalculator:

    @staticmethod
    def calculate(pizza: Pizza) -> float:
        price = pizza.base_price
        for topping_type, qty in pizza.toppings.items():
            topping = ToppingFactory.create(topping_type)
            price += topping.price_per_serving() * qty

        return PriceRuleEngine.apply(pizza, price)


class PizzaBuilder:
    def __init__(self):
        self._size = None
        self._toppings = {}

    def size(self, size: PizzaSize):
        self._size = size
        return self
    
    def add_topping(self, topping: ToppingType, qty: int = 1):
        if self._size == PizzaSize.SMALL and topping == ToppingType.CHEESE_BURST:
            raise ValueError("Cheese Burst not allowed on Small Pizza")
        self._toppings[topping] = self._toppings.get(topping, 0) + qty
        return self
    
    def build(self) -> Pizza:
        if not self._size:
            raise ValueError('Pizza size is required')
        return Pizza(self._size, self._toppings)
    
pizza = (
    PizzaBuilder()
    .size(PizzaSize.MEDIUM)
    .add_topping(ToppingType.CORN, 3)
    .add_topping(ToppingType.CHEESE_BURST, 1)
    .build()
)
pizza.add_toppings(ToppingType.CHEESE_BURST, 1)
total = PriceCalculator.calculate(pizza)
print(f"Total price: {total}")

'''
Staff-Level Summary (Say This)

“I used Builder Pattern to enforce creation-time validation, Strategy pattern for pricing rules, and a rule engine to keep pricing extensible and open–closed.”
'''



# from enum import Enum
# from typing import defaultdict
# from abc import ABC, abstractmethod

# class PizzaSize(Enum):
#     SMALL = 1
#     MEDIUM = 2
#     LARGE = 3

# class ToppingType(Enum):
#     CORN = 1
#     ONION = 2
#     CHEESE_BURST = 3

# pizzaPrice = {PizzaSize.SMALL: 100, PizzaSize.MEDIUM: 150, PizzaSize.LARGE: 200}

# class Pizza:
#     def __init__(self, size):
#         self.size = size
#         self.basePrice = pizzaPrice[size]
#         self.toppings = defaultdict(int)

#     def addToping(self, topping: ToppingType, serving: int):
#         self.toppings[topping] += serving

#     def getSize(self) -> PizzaSize:
#         return self.size
    
#     def getBasePrice(self) -> float:
#         return self.basePrice
    
#     def getToppings(self):
#         return self.toppings

# class Topping(ABC):

#     def getType(self) -> ToppingType:
#         pass

#     def pricePerServing(self) -> float:
#         pass

# class CornTopping(Topping):
#     def getType(self) -> ToppingType:
#         return ToppingType.CORN
    
#     def pricePerServing(self) -> float:
#         return 30
    
# class OnionTopping(Topping):
#     def getType(self) -> ToppingType:
#         return ToppingType.ONION
    
#     def pricePerServing(self) -> float:
#         return 20

# class CheeseBurstTopping(Topping):
#     def getType(self) -> ToppingType:
#         return ToppingType.CHEESE_BURST
    
#     def pricePerServing(self) -> float:
#         return 50

# # class PriceRuleEngine:

# #     @staticmethod
# #     def validate(pizza):
# #         if pizza.getSize() == PizzaSize.SMALL and ToppingType.CHEESE_BURST in pizza.getToppings():
# #             return False
# #         return True
    
# #     @staticmethod
# #     def applyDiscount(topping: ToppingType, serving: int, original: float) -> float :
# #         if topping == ToppingType.CORN and serving >= 2:
# #             return original * 0.7
# #         return original

# class ToppingFactory:

#     @staticmethod
#     def create(topping_type: ToppingType):
#         match topping_type:
#             case ToppingType.CORN:
#                 return CornTopping()
#             case ToppingType.ONION:
#                 return OnionTopping()
#             case ToppingType.CHEESE_BURST:
#                 return CheeseBurstTopping()
            
# class DiscountStrategy(ABC):

#     @abstractmethod
#     def apply(cost: float, quantity: int) -> float:
#         pass

# class CornDiscountStrategy(DiscountStrategy):
#      def apply(cost: float, quantity: int) -> float:
#         return cost * 0.7 if quantity >= 2 else cost

# class OnionDiscountStrategy(DiscountStrategy):
#      def apply(cost: float, quantity: int) -> float:
#         return cost

# class CheeseBurstDiscountStrategy(DiscountStrategy):
#      def apply(cost: float, quantity: int) -> float:
#         return cost * 0.8 if quantity >= 2 else cost


# class Rule(ABC):
    
#     @abstractmethod
#     def validate(pizza: Pizza) -> bool:
#         pass

# class CornRule(Rule):
    
#     def validate(pizza: Pizza) -> bool:
#         return True if pizza.getToppings()[ToppingType.CORN] >= 2 else False

# class PricingRule(ABC):
#     @abstractmethod
#     def isApplicable(self, pizza: Pizza) -> bool:
#         pass

#     @abstractmethod
#     def apply(self, pizza: Pizza, currentPrice: float) -> float:
#         pass

# class CornBulkDiscountRule(PricingRule):
#     def isApplicable(self, pizza: Pizza) -> bool:
#         return True if pizza.getToppings()[ToppingType.CORN] >= 2 else False

#     def apply(self, pizza: Pizza, currentPrice: float) -> float:
#         serving = pizza.getToppings()[ToppingType.CORN]
#         cornPrice = serving * 30
#         return currentPrice - (cornPrice * 0.3)

# class CheeseCornComboRule(PricingRule):
#     def isApplicable(self, pizza: Pizza) -> bool:
#         toppings = pizza.getToppings()
#         if ToppingType.CORN in toppings and ToppingType.CHEESE_BURST in toppings and pizza.getSize() != PizzaSize.SMALL:
#             return True
#         return False

#     def apply(self, pizza: Pizza, currentPrice: float) -> float:
#         return currentPrice - 20   

# class PriceRuleEngine:

#     rules = [CornBulkDiscountRule(), CheeseCornComboRule()]

#     @staticmethod
#     def applyRule(pizza: Pizza, basePrice: float) -> float :
#         price = basePrice
#         for rule in PriceRuleEngine.rules:
#             if rule.isApplicable(pizza) :
#                 price = rule.apply(pizza, price)
#         return price



# # class PriceCalculator:
# #     def __init__(self):
# #         self.toppingMap = {ToppingType.CORN: CornTopping(), ToppingType.ONION: OnionTopping(), ToppingType.CHEESE_BURST: CheeseBurstTopping()}

# #     def calculatePrice(self, pizza: Pizza) -> float:
# #         if not PriceRuleEngine.validate(pizza):
# #             print("topping not applicable")
# #             return -1.0
# #         total = pizza.getBasePrice()
# #         for topping_type, serving in pizza.getToppings().items():
# #             topping_price = self.toppingMap[topping_type].pricePerServing() * serving
# #             print(f"base price: {total} topping_price: {topping_price}")
# #             cost = PriceRuleEngine.applyDiscount(topping_type, serving, topping_price)
# #             total += cost
# #             print(f"total : {total}, cost:{cost}")

# #         return total

# class PriceCalculator:

#     @staticmethod
#     def calculatePrice(pizza: Pizza) -> float:
#         price = pizza.getBasePrice()
#         for topping_type, serving in pizza.getToppings().items():
#             topping = ToppingFactory.create(topping_type)
#             price += topping.pricePerServing() * serving

#         return PriceRuleEngine.applyRule(pizza, price)


# pizza = Pizza(PizzaSize.MEDIUM)
# pizza.addToping(ToppingType.CORN, 3)
# pizza.addToping(ToppingType.CHEESE_BURST, 1)
# total = PriceCalculator.calculatePrice(pizza)
# print(f"total price: {total}")