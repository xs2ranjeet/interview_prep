'''
506. Pacific and Atlantic Water Flow
Medium
You are given an NxM rectangular island divided into a grid of cells, where each cell has a certain height representing 
its elevation. The island is bordered by the Pacific Ocean to the top and left and the Atlantic Ocean to the bottom and right. 
The island receives rainfall, and water can flow from a cell to its neighboring cell if the neighboring cell's height 
is less than or equal to the current cell's height. Your task is to find and return a list of coordinates from which water 
can flow to both the Pacific Ocean and the Atlantic Ocean.

Input:

A 2D grid representing the island with elevation heights.
1 <= N, M <= 200
0 <= height of a cell <= 10^5
Output:

A list of coordinates (row, column) representing cells from which water can flow to both the Pacific and Atlantic Oceans.
Example:

Input:
island = [
    [1, 2, 2, 3, 5],
    [3, 2, 3, 4, 4],
    [2, 4, 5, 3, 1],
    [6, 7, 1, 4, 5],
    [5, 1, 1, 2, 4]
]

Output:
[(0, 4), (1, 3), (1, 4), (2, 2), (3, 0), (3, 1), (4, 0)]

'''

class Solution:
    from typing import List
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m, n = len(heights), len(heights[0])
        pacific = [[False] * n for _ in range(m)]
        atlanta = [[False] * n for _ in range(m)]
        dirs = [-1, 0, 1, 0, -1]
        def dfs(i: int, j: int, visited: List[List[bool]]):
            visited[i][j] = True
            for k in range(4):
                nx, ny = i + dirs[k], j + dirs[k+1]
                if nx >= 0 and ny >= 0 and nx < m and ny < n and visited[nx][ny] == False and heights[nx][ny] >= heights[i][j]:
                    dfs(nx, ny, visited)

        
        for i in range(m):
            dfs(i, 0, pacific)
            dfs(i, n-1,  atlanta)
        
        for j in range(n):
            dfs(0,j, pacific)
            dfs(m-1, j, atlanta)

        result = []
        for i in range(m):
            for j in range(n):
                if pacific[i][j] and atlanta[i][j]:
                    result.append([i, j])
        return result

