'''
2754. Maximum Points by Deleting Numbers | Delete and Earn
Coding and Problem-SolvingData Structures & Algorithms (DSA)ArraysDynamic Programming (DP)
Medium
You are given an integer array nums. You can perform the following operation any number of times:

Choose any element x from the array.
Earn x points.
Delete all occurrences of x from the array as well as every element equal to x - 1 and x + 1.
Return the maximum total points you can earn after applying the operation optimally.

Input Format:
First line: an integer n, the size of the array.
Second line: n space‑separated integers representing nums.
Output Format:
A single integer — the maximum points obtainable.
Example 1:
Input:
6
3 4 2 3 3 4

Output:
10
Explanation

Option 1: Choose the value 3 first. You earn 3 points and delete all 2s and 4s. The remaining array is [3, 3], Delete 3 2 times again again, your earning becomes total 9.
Option 2: A better sequence is to delete all 4s first (earning 8 points) and then delete the remaining 2 (earning 2 points), for a total of 10 points. The optimal total is 10.
Constraints:
1 <= n <= 2 * 10^4
1 <= nums[i] <= 10^5

'''
from typing import List
from collections import Counter

def deleteAndEarn(nums: List[int]) -> int :
    counter = Counter(nums)
    # arr = sorted([key for key,_ in counter.items()])
    arr = sorted(counter.keys())
    n = len(arr)
    dp = [0] * (n+1)
    dp[1] = arr[0] * counter[arr[0]]
    for i in range(2, n+1):
        dp[i] = arr[i-1] * counter[arr[i-1]]
        if arr[i-1] != (arr[i-2] + 1):
            dp[i] += dp[i-1]
        else:
            dp[i] = max(dp[i-1], dp[i] + dp[i-2])

    # print(arr)
    # print(counter)
    # print(dp)
    return dp[n]

def deleteAndEarn2(nums: List[int]) -> int :
    counter = Counter(nums)
    arr = sorted(counter.keys())
    prev, curr = 0, arr[0] * counter[arr[0]]
    for i in range(1, len(arr)):
        value = arr[i] * counter[arr[i]]
        if arr[i] == arr[i-1] + 1:
            prev, curr = curr, max(curr, prev + value)
        else:
            prev, curr = curr, curr + value
    return curr

nums = [3, 4, 2, 3, 3, 4]
print(f"{deleteAndEarn2(nums)}") 
