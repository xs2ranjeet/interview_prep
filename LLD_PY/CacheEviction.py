from typing import List, Dict, Set
import threading
from abc import ABC, abstractmethod
from typing import DefaultDict, OrderedDict

class Storage(ABC):
    
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def contains(self, key) -> bool:
        pass

class InMemoryStorage(Storage):
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key, None)
        
    def put(self, key, value):
        self.store[key] = value

    def remove(self, key):
        self.store.pop(key, None)

    def contains(self, key):
        return key in self.store
    

class EvictionPolicy(ABC):
    @abstractmethod
    def on_get(self, key):
        pass

    @abstractmethod
    def on_put(self, key):
        pass

    @abstractmethod
    def evict(self, key):
        pass

    @abstractmethod
    def contains(self, key):
        pass


class LRUEvictionPolicy(EvictionPolicy):
    def __init__(self):
        self.keys = OrderedDict()

    def on_get(self, key):
        self.keys.move_to_end(key, last=False)

    def on_put(self, key):
        self.keys[key] = True

    def evict(self):
        if self.keys:
            self.keys.popitem(last=False)

    def contains(self, key):
        return key in self.keys
  


class CacheEngine:
    def __init__(self, storage: Storage, eviciton)
