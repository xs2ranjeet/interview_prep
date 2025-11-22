'''
27. Top K Frequent Strings | K Most Frequent Words
https://enginebogie.com/public/question/top-k-frequent-strings-k-most-frequent-words/27
Medium
Given a list of strings strings[] and an integer k, find top k most frequent strings.

Return strings in decreasing order of their frequency. If the two strings have the same frequency, then sort them using lexicographical order.

Example 1:

Input: 
strings[] = ["this", "is", "engine", "bogie", "best", "mentorship","platform","is","engine","bogie"],
k = 2

Output: ["bogie", "engine', "is", ]
'''
from typing import List
from collections import Counter, defaultdict
import heapq

def topKWords(strings: List[str], k: int):
    freq = Counter(strings)
    print(freq)
    heap = []
    for word, count in freq.items():
        heapq.heappush(heap, (count, word))
        if len(heap) > k:
            heapq.heappop(heap)
    result = []
    while heap:
        count, word = heapq.heappop(heap)
        result.append((count, word))
    result.sort(key=lambda x: (-x[0], x[1]))
    return [word for _, word in result]

strings= ["this", "is", "engine", "bogie", "best", "mentorship","platform","is","engine","bogie"]
k = 2

print(f"{topKWords(strings, k)}")