'''
286. Next Greater Element
Next Greater Element
Mediumhttps://enginebogie.com/public/question/next-greater-element/286
Given an array of integers, your task is to find the next greater element to the right of every element in the array. The next greater element is the first element to the right that is greater than the current element. If there is no such element, consider it as -1.

Write a function or algorithm to find the next greater element to the right of each element in the array and return the resulting array.

Example 1:

Input: [4, 6, 3, 2, 8, 1]
Output: [6, 8, 8, 8, -1, -1]
Explanation: 
- For the element 4, the next greater element to its right is 6.
- For the element 6, the next greater element to its right is 8.
- For the element 3, the next greater element to its right is 8.
- For the element 2, the next greater element to its right is 8.
- For the element 8, there is no greater element to its right, so it is -1.
- For the element 1, there is no greater element to its right, so it is -1.
Note:

The input array contains distinct integers.
If there is no greater element to the right of an element, consider it as -1.
'''

from typing import List

def nextGreaterNumber(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [-1] *n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] <= nums[i]:
            index = stack[-1]
            stack.pop()
            result[index] = nums[i]
        stack.append(i)
    return result

nums = [4, 6, 3, 2, 8, 1]
print(f"{nextGreaterNumber(nums)}")