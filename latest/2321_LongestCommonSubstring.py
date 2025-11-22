'''
2321. Longest Common Substring
https://enginebogie.com/interview/experience/salesforce-software-development-engineer/771
Coding and Problem-SolvingData Structures & Algorithms (DSA)StringDynamic Programming (DP)
Medium
Given two strings, s1 and s2, find the length of the longest common substring. 
A substring must consist of contiguous characters from the original string.

Input Format:
Two strings, s1 and s2.

Output Format:
An integer representing the length of the longest common substring.

Example 1:
Input:
s1 = "abcdefg"
s2 = "xyzcdef"

Output:
4

Explanation
The longest common substring is "cdef", which has a length of 4.
'''

def longestCommonSubstring(s1: str, s2: str) -> str :
    if not s1 or not s2:
        return ""
    
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    start, maxLen = 0, 0

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = 0
            if maxLen < dp[i][j]:
                maxLen = dp[i][j]
                start = i - maxLen
    print(f"{maxLen} , {start}")
    return s1[start: start+ maxLen]

def longestCommonSubstring2(s1: str, s2: str) -> str :
    if not s1 or not s2:
        return ""
    m,n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    start, maxLen = 0, 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                curr[j] = 1 + prev[j-1]
            else:
                curr[j] = 0
            if maxLen < curr[j] :
                maxLen = curr[j]
                start = i - maxLen
        prev, curr= curr, prev
    print(f"{maxLen} , {start}")
    return s1[start: start + maxLen]

s1 = "abcdefg"
s2 = "xyzcdef"

print(f"{longestCommonSubstring2(s1, s2)}")