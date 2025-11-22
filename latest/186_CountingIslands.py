'''
186. Counting Number of Islands
https://enginebogie.com/public/question/counting-number-of-islands/186
Medium
Given a binary 2D grid of size r x c where r represents number of rows and c represents number of columns. 
In this grid, 1 represents the presence of land and 0 represents presence of water at that location.

An island is formed by connecting adjacent lands horizontally or vertically and is surrounded by water.
 You may assume all four edges of the grid are all surrounded by water.

Given such a grid, find the number of Islands present in it.

Example 1:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
Example 2:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
'''
from typing import List
from collections import deque

def countIslands(grid:List[List[str]]) -> int :
    m, n = len(grid), len(grid[0])
    dirs = [-1, 0, 1, 0, -1]

    def dfs(i: int, j: int):
        grid[i][j] = "2"

        for k in range(4):
            nx, ny = i + dirs[k], j + dirs[k+1]
            if nx >=0 and ny >=0 and nx < m and ny < n and grid[nx][ny] == "1":
                dfs(nx, ny)

    count = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "1":
                dfs(i, j)
                count += 1

    for i in range(m):
        for j in range(n):
            if grid[i][j] == "2":
                grid[i][j] = "1"
                
    return count


grid1 = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
print(f"{countIslands(grid)}")