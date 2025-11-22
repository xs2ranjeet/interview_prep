'''
1793. Profile Visibility in a Social Media Network
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/381
Coding and Problem-SolvingData Structures & Algorithms (DSA)GraphConnected ComponentsDepth-First Search (DFS)Breadth-First Search (BFS)Disjoint Set Union (Union-Find)
Medium
A popular social media platform allows users to connect with each other. The connections are represented as an undirected graph where:

Each node is a user (numbered from 1 to N).
Each edge (u, v) means that user u is directly connected to user v.
A user can view:

Their own profile.
Profiles of all users directly or indirectly connected to them.
You are given:

Two arrays u and v of equal length, representing the connections.
A list queries containing user IDs.
For each user in queries, return the number of profiles they can view. The output should be in the same order as the queries.

Example 1:
Input:
u = [2, 1, 4, 5]
v = [1, 3, 5, 6]
queries = [1, 5, 7]

Output:
[3, 3, 1]

Explanation:
The graph connections are:
(2 - 1), (1 - 3), (4 - 5), (5 - 6)

Connected components:
1 ↔ 2 ↔ 3  (size = 3)
4 ↔ 5 ↔ 6  (size = 3)
7          (size = 1)

Query results:
1 → in component of size 3 → 3
5 → in component of size 3 → 3
7 → in component of size 1 → 1
Example 2:
Input:
u = [1, 2, 3, 8, 9]
v = [2, 3, 4, 9, 10]
queries = [1, 8, 5]

Output:
[4, 3, 1]

Explanation:
Graph connections:
(1 - 2), (2 - 3), (3 - 4) → component size = 4
(8 - 9), (9 - 10) → component size = 3
(5) → size = 1

Queries:
1 → component size 4
8 → component size 3
5 → size 1
Constraints:

1 ≤ N ≤ 10^5 (total number of distinct users)
1 ≤ len(u), len(v) ≤ 10^5
1 ≤ u[i], v[i] ≤ N
1 ≤ len(queries) ≤ 10^5
Graph can be disconnected.
No duplicate self-loops, but multiple edges between the same nodes may exist.
'''
from typing import List

class DSU:
    def __init__(self, n):
        self.parent = [x for x in range(n+1)]
        self.size = [1] *(n+1)

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if(px == py):
            return
        if self.size[px] >= self.size[py]:
            self.parent[py] = px
            self.size[px] += self.size[py]
        else:
            self.parent[px] = py
            self.size[py] += self.size[px]

    def getSize(self, x):
        return self.size[self.find(x)]


def profileVisibility(u: List[int], v: List[int], queries: List[int]) -> List[int]:
    n = max(max(u), max(v), max(queries))
    dsu = DSU(n)
    for uu, vv in zip(u, v):
        dsu.union(uu, vv)

    result = [dsu.getSize(x) for x in queries]
    return result
    

u = [1, 2, 3, 8, 9]
v = [2, 3, 4, 9, 10]
queries = [1, 8, 5]

# u = [2, 1, 4, 5]
# v = [1, 3, 5, 6]
# queries = [1, 5, 7]

result = profileVisibility(u, v, queries)
print(result)