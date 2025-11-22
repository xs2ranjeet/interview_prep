'''
827. Low-Level Design: Design & Implement LFU Cache
https://enginebogie.com/interview/experience/salesforce-principal-member-of-technical-staff/407
CachingLow-Level Design (LLD)Design PatternsSOLIDClean CodingStrategy Design PatternLeast Frequently Used (LFU)
Medium
Design and implement a Least Frequently Used (LFU) Cache. The cache should store key value pairs and 
should have the following behavior:

When the cache reaches its capacity and a new item needs to be added, it should remove the item with the lowest usage frequency.
If multiple items have the same lowest frequency, the one that was used least recently should be removed.
The cache should support the following operations efficiently:
get(key): Return the value if the key exists in the cache, otherwise return -1.
put(key, value): Insert or update the value of the key. If the cache is full, evict one item as per the LFU policy.
Example behavior:

cache = LFUCache(2)
cache.put(1, 10)
cache.put(2, 20)
cache.get(1)     // returns 10
cache.put(3, 30) // evicts key 2
cache.get(2)     // returns -1
cache.get(3)     // returns 30
'''
from collections import defaultdict, OrderedDict

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
       # self.next = None
       # self.prev = None

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.minFreq = 0
        self.key2Node = {}
        self.freq2dll = defaultdict(OrderedDict)

    def get(self, key) -> int :
        if key not in self.key2Node:
            return -1
        node = self.key2Node[key]
        self._update(node)
        return node.value
    
    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.key2Node:
            node = self.key2Node[key]
            node.value = value
            self._update(node)
            return
        # Need to evict
        if len(self.key2Node) == self.capacity:
            oldKey, oldNode = self.freq2dll[self.minFreq].popitem(last=False)
            del self.key2Node[oldKey]
        node = Node(key, value)
        self.key2Node[key] = node
        self.freq2dll[1][key] = node
        self.minFreq = 1

    def _update(self, node: Node):
        freq = node.freq
        del self.freq2dll[freq][node.key]
        if not self.freq2dll[freq]:
            del self.freq2dll[freq]
            if freq == self.minFreq:
                self.minFreq += 1
        node.freq += 1
        self.freq2dll[node.freq][node.key] = node

cache = LFUCache(2)
cache.put(1, 10)
cache.put(2, 20)
print(cache.get(1))     #returns 10
cache.put(3, 30) # evicts key 2
print(cache.get(2))     # returns -1
print(cache.get(3))     # returns 30