'''
282. Lexicographically Largest Valid Sequence
https://enginebogie.com/public/question/lexicographically-largest-valid-sequence/282
Medium
Given a positive integer N, the task is to construct the lexicographically largest valid sequence of length N. A valid sequence is defined as a sequence of distinct positive integers where for every i-th index (1 ≤ i ≤ N), the following conditions hold:

The number at i-th index is divisible by i.
The number at i-th index is not divisible by any number from 2 to (i-1).
Example 1:

Input: N = 3
Output: [3, 1, 2]
Explanation: The sequence [3, 1, 2] is lexicographically largest and satisfies all the conditions. The number at index 1 is divisible by 1, the number at index 2 is divisible by 2, and the number at index 3 is divisible by 3.
Example 2:

Input: N = 6
Output: [6, 1, 5, 2, 4, 3]
Explanation: The sequence [6, 1, 5, 2, 4, 3] is lexicographically largest and satisfies all the conditions. The numbers at each index are divisible by their corresponding indices and are not divisible by any number before them in the sequence.
Salesforce
'''