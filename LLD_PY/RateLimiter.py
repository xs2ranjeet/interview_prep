import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def allow_request(self):
        current_time = time.time()

        while self.requests and current_time - self.requests[0] >= self.time_window:
            self.requests.popleft()

        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False
    
limiter = RateLimiter(max_requests = 5, time_window=60)
for i in range(10):
    if limiter.allow_request():
        print(f"Request {i+1}: Allowed")
    else:
        print(f"Request {i+1}: Rate limited")