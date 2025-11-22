'''
59. Find Top N Frequent Elements in a Repeating Integer Array
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/237
Coding and Problem-SolvingData Structures & Algorithms (DSA)ArraysHeapPriority QueueHash TableSorting
Medium
Given an array of integers where some numbers might be appearing more than once, write a function that identifies the top N most frequent elements in the array. The result should be sorted in descending order of frequency, and if two elements have the same frequency, they should be sorted by their value in ascending order.

Input:
An array of integers nums, which may contain both positive and negative numbers and could include duplicates. An integer N, representing the number of top frequent elements to return.

Output:
A list of integers representing the top N frequent elements, sorted first by their frequency (in descending order) and then by their value (in ascending order) if frequencies are equal.

Constraints:
1 <= nums.length <= 10^5 -10^5 <= nums[i] <= 10^5 The array nums is not necessarily sorted. 1 <= N <= number of unique elements in nums

Example 1:
Input: nums = [3, 1, 2, 2, 4, 3, 5], N = 2
Output: [2, 3]
Explanation: The numbers 2 and 3 both appear twice in the array which is the highest frequency, making them the top 2 most frequent elements. They are returned in ascending order of their values.
Example 2:
Input: nums = [1], N = 1
Output: [1]
Explanation: With only one number in the array, it is trivially the most frequent element.
Example 3:
Input: nums = [4, 1, 2, 2, 3, 3, 3, 4, 4, 4], N = 3
Output: [4, 3, 2]
Explanation: The number 4 appears 4 times, 3 appears 3 times, and 2 appears 2 times. These are the three most frequent numbers, sorted by their frequency and then by value.


'''
from typing import List
from collections import Counter
import heapq

def topNFrequent(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    minHeap = []

    for num, count in freq.items():
         # Push tuple: -count for max-heap effect; num for tiebreaker
        heapq.heappush(minHeap, (-count, num))

    # Extract top N elements and sort as per requirement
    top = [heapq.heappop(minHeap) for _ in range(k)]
    # Final sorting: frequency desc, value asc (already sorted by heap, but double-sort for clarity)
    top_sorted = sorted(top, key=lambda x: (x[0], x[1]))
    return [num for _, num in top_sorted]
    # result = []
    # while minHeap:
    #     freq, key = heapq.heappop(minHeap)
    #     result.append(key)
    # result.reverse()
    # return result

nums1 = [3, 1, 2, 2, 4, 3, 5]
N1 = 2
#Output: [2, 3]
nums2 = [1]
N2 = 1
#Output: [1]

nums3 = [4, 1, 2, 2, 3, 3, 3, 4, 4, 4]
N3 = 3
#Output: [4, 3, 2]

print(f"{topNFrequent(nums1, N1)}")
print(f"{topNFrequent(nums2, N2)}")
print(f"{topNFrequent(nums3, N3)}")