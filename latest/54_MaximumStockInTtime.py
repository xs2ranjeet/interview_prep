'''
54. Maximum stock price in last t minutes
Hard
I will be receiving some stock prices. I have a given windowsTime as well. Whenever a stock price is provided, I need to tell the maximum stock price seen in the last windowsTime seconds.
You’re given:
https://enginebogie.com/public/question/maximum-stock-price-in-last-t-minutes/54
A stream of stock prices arriving over time.
A fixed window size windowsTime (in seconds).
For each new price, you need to report the maximum stock price seen in the last windowsTime seconds.
Efficiently maintaining the maximum in a sliding time window.
Handling continuous updates without recomputing from scratch.
Ensuring scalability for large input streams.
'''

from collections import deque
import time

class StockWindow:
    def __init__(self, window_time):
        self.window_time = window_time
        self.deque = deque()

    def add_price(self, price, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        # Remove smaller elements from the back
        while self.deque and self.deque[-1][0] <= price:
            self.deque.pop()

        # Add new price
        self.deque.append((price, timestamp))

        # Remove outdated elements from the front
        while self.deque and timestamp - self.deque[0][1] > self.window_time:
            self.deque.popleft()

    def get_max(self):
        return self.deque[0][0] if self.deque else None
