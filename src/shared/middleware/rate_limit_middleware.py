
from datetime import time


class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
        
    def is_allowed(self, user_id: str) -> bool:
        if user_id not in self.requests:
            self.requests[user_id] = []
        current_time = time.time()
        self.requests[user_id] = [time for time in self.requests[user_id] if time > current_time - self.time_window]
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            return True
        return False