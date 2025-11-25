'''
887. Super Egg Drop
https://leetcode.com/problems/super-egg-drop/description/
You are given k identical eggs and you have access to a building with n floors labeled from 1 to n.
You know that there exists a floor f where 0 <= f <= n such that any egg dropped at a floor higher than f will break, and any egg dropped at or below floor f will not break.
Each move, you may take an unbroken egg and drop it from any floor x (where 1 <= x <= n). If the egg breaks, you can no longer use it. However, if the egg does not break, you may reuse it in future moves.
Return the minimum number of moves that you need to determine with certainty what the value of f is.

Example 1:

Input: k = 1, n = 2
Output: 2
Explanation: 
Drop the egg from floor 1. If it breaks, we know that f = 0.
Otherwise, drop the egg from floor 2. If it breaks, we know that f = 1.
If it does not break, then we know f = 2.
Hence, we need at minimum 2 moves to determine with certainty what the value of f is.
Example 2:

Input: k = 2, n = 6
Output: 3
Example 3:

Input: k = 3, n = 14
Output: 4
 

Constraints:

1 <= k <= 100
1 <= n <= 104
'''
def superEggDrop(k: int, n: int) -> int:
    memo = {}
    def min_moves(eggs: int, floors: int) -> int:
        if floors == 0:
            return 0 
        if eggs == 1:
            return floors
        if (eggs, floors) in memo:
            return memo[(eggs, floors)]
        min_attempt = float('inf')
        low, high = 1, floors
        while low <= high:
            mid  = low + (high - low)//2
            broken = min_moves(eggs -1, mid - 1)
            not_broken = min_moves(eggs, floors - mid)
            worst_case = 1 + max(broken, not_broken)
            min_attempt = min(min_attempt, worst_case)
            if broken < not_broken:
                low = mid +1  # move up, egg didn't break
            else:
                high = mid -1
        memo[(eggs, floors)] = min_attempt
        return min_attempt
    return min_moves(k, n)

print(f"{superEggDrop(2, 6)}")
print(f"{superEggDrop(3, 14)}")