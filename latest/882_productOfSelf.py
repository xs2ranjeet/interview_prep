'''
882. Product of Array Except Self
Medium
You are given an integer array nums. Your task is to create a new array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example:

Input: nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Explanation:
- For the element at index 0, the product except itself is 2*3*4 = 24.
- For the element at index 1, the product except itself is 1*3*4 = 12.
- For the element at index 2, the product except itself is 1*2*4 = 8.
- For the element at index 3, the product except itself is 1*2*3 = 6.

'''
from typing import List

def productOfArray(nums: List[int]) -> List[int]:
    n = len(nums)
    zcount = 0
    product = 1
    for i in range(n):
        if nums[i] == 0:
            zcount += 1
        else:
            product *= nums[i]
        if zcount == 2:
            break
    result = [0] *n
    if zcount == 2:
        return result
    
    for i in range(n):
        if zcount == 0:
            result[i] = product // nums[i]
        elif nums[i] == 0:
            result[i] = product
    return result

nums = [1, 2, 0, 3, 4]
print(f"{productOfArray(nums)}")
