'''
881. Target Sum | Number of Different Ways to Reach Target Sum
Medium
You are given an array of integers, nums, and an integer target. Your task is to determine the number of different ways to add the symbols '+' and '-' before each integer in nums such that when the integers are concatenated into an expression, the resulting value equals the target.

For instance, if nums = [2, 1], you can create the following expressions: "+2+1", "+2-1", "-2+1", and "-2-1". Each expression represents a different way to assign '+' or '-' to the numbers such that their algebraic sum is calculated.

Example 1:

Input: nums = [1, 1, 1, 1, 1], target = 3
Output: 5

Explanation:
+1+1+1-1+1 = 3
+1+1-1+1+1 = 3
+1-1+1+1+1 = 3
-1+1+1+1+1 = 3
+1+1+1+1-1 = 3
There are 5 ways to assign symbols to get the sum of 3.
Example 2:

Input: nums = [1], target = 1
Output: 1

Explanation:
+1 = 1
There is 1 way to assign a symbol to get the sum of 1.
'''
from typing import List

def wayTargetSum(nums: List[int], tsum: int) -> int :
    memo = {}

    def helper(index: int, csum: int) -> int:
        if(index == len(nums)):
            return 1 if  csum == tsum else 0
        if (index, csum) in memo:
            return memo[(index, csum)]
        memo[(index, csum)] = helper(index + 1, csum - nums[index]) + helper(index + 1, csum + nums[index])
        return memo[(index, csum)]
    return helper(0,0)
    
nums = [1, 1, 1, 1, 1]
target = 3
print(f"{wayTargetSum(nums, target)}")