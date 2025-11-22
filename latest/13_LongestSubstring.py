'''
13. Longest Substring Without Repeating Characters
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/381
Coding and Problem-SolvingData Structures & Algorithms (DSA)StringSliding WindowTwo PointerHashing
Medium
Given a string str, find the length of the longest substring without repeating characters.

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
Example 4:

Input: s = ""
Output: 0

Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.
'''

def longestSubstring(s: str): 
    if not s:
        return 0
    indexMap = {}
    left =  0
    maxlen = 0
    for right, ch in enumerate(s):
        if ch in indexMap and indexMap[ch] >= left:
            left = indexMap[ch] + 1
        maxlen = max(maxlen, right -left + 1)
        indexMap[ch] = right
    return maxlen


print(f"{longestSubstring("abcabcbb")}")
print(f"{longestSubstring("bbbbb")}")
print(f"{longestSubstring("pwwkew")}")
print(f"{longestSubstring("")}")