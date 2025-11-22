'''
2515. House Robber
Medium
You are a professional robber planning to rob houses along a street. Each house contains a certain amount of money. The only restriction is that you cannot rob two directly adjacent houses, because their security systems are linked and will alert the police.

Your goal is to choose a subset of houses to rob such that the total amount of money is maximized while never picking two neighboring houses.

Input Format:
First line: an integer n, the number of houses.
Second line: n space‑separated integers nums[i] representing the money in each house.
Output Format:
A single integer — the maximum amount of money you can rob.
Example 1:
Input:
4
1 2 3 1
Output:
4
Explanation Rob house 1 (money = 1) and house 3 (money = 3) for a total of 4.

Example 2:
Input:
5
2 7 9 3 2
Output:
13
Explanation Rob houses 1, 3 and 5 for a total of 13.

Constraints:
1 <= n <= 100
0 <= nums[i] <= 400
'''
from typing import List

def rob(houses: List[int]) -> int :
    n = len(houses)
    if n == 0:
        return 0
    if n == 1:
        return houses[0]
    if n == 2:
        return max(houses[0], houses[1])
    dp = [0] * (n+1)
    dp[1] = houses[0]
    for i in range(2, n+1):
        dp[i] = max(houses[i-1] + dp[i-2], dp[i-1])
    return dp[n]

houses = [2, 7, 9, 3, 2]
print(f"{rob(houses)}")