from typing import List
from collections import deque

class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        colors = [-1] *n
        for i in range(n):
            if colors[i] != -1:
                continue
            colors[i] = 0
            deq = deque()
            deq.append(i)
            while deq:
                curr = deq.popleft()
                for nbr in graph[curr]:
                    if colors[nbr] == -1:
                        colors[nbr] = 1 - colors[curr]
                        deq.append(nbr)
                    elif colors[nbr] == colors[curr]:
                        return False
        return True
    
    def isBipartite2(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        colors = [-1] *n
        for i in range(n):
            if colors[i] != -1:
                continue
            stack = []
            stack.append(i)
            colors[i] = 0
            while stack:
                curr = stack.pop()
                for nbr in graph[curr]:
                    if colors[nbr] == -1:
                        colors[nbr] = 1 - colors[curr]
                        stack.append(nbr)
                    elif colors[nbr] == colors[curr]:
                        return False
        return True

graph = [[1,3],[0,2],[1,3],[0,2]]

sol = Solution()
print(sol.isBipartite2(graph))
