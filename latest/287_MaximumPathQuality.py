'''
287. Maximum Path Quality of a Graph
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/237
GraphBacktrackingArraysCoding and Problem-SolvingAlgorithmsData Structures
Hard
You are given an undirected graph with positive edge weights. The quality of a path in the graph is defined 
as the minimum weight among all the edges in that path. Your task is to find the maximum quality among all possible paths in the graph.

Example 1:

Input:
Graph:
 

Edges and Weights:
- (A, B) -> 5
- (A, C) -> 3
- (C, B) -> 2
- (C, D) -> 4
- (B, E) -> 6
- (B, F) -> 7
- (E, F) -> 3
- (F, G) -> 2
- (G, H) -> 4
- (C, H) -> 1

Output: 5
Explanation: The maximum quality path is A -> B -> F -> G -> H with a minimum weight of 5.
Note:

The graph is represented as a set of vertices and edges with associated weights.
The graph can have cycles and disconnected components.
The maximum quality path refers to the path with the highest minimum weight among all paths in the graph.
'''
class DSU:
    def __init__(self, n):
        self.count = n
        self.parent = list(range(n))
        self.rank = [0] * (n)

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] > self.rank[py]:
            self.parent[py] = px
        elif self.rank[py] > self.rank[px]:
            self.parent[px] = py
        else:
            self.parent[py] = px
            self.rank[px] += 1
        self.count -= 1
        return True
    
def maximumPathQuality(n, edges) -> int:
    dsu = DSU(n)
    edges.sort(key=lambda x: x[-2])
    for u, v, wt in edges:
        dsu.union(u, v)

        # When graph becomes fully connected
        if dsu.count == 1:
            return wt  # bottleneck weight
    return 0
    

edges = [
    ("A", "B", 5),
    ("A", "C", 3),
    ("C", "B", 2),
    ("C", "D", 4),
    ("B", "E", 6),
    ("B", "F", 7),
    ("E", "F", 3),
    ("F", "G", 2),
    ("G", "H", 4),
    ("C", "H", 1)
]

# Map nodes to indices
nodes = list({u for u,v,_ in edges} | {v for u,v,_ in edges})
node_id = {node: i for i,node in enumerate(nodes)}

edges_num = [(node_id[u], node_id[v], w) for u,v,w in edges]
print(maximumPathQuality(len(nodes), edges_num))  # Output: 5

        