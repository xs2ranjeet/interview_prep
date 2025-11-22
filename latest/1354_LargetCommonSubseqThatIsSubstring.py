'''
1354. Longest Common Subsequence that is also a Substring
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/237
Coding and Problem-SolvingData Structures & Algorithms (DSA)LCSDynamic Programming (DP)
Medium
You are given two strings:

s1 (of length n)
s2 (of length m)
Your task is to find the length of the longest string s3, such that:

s3 is a subsequence of s1.
s3 is a substring of s2.
Definitions:

A subsequence of a string is formed by deleting zero or more characters while maintaining the relative order of the remaining characters.
A substring of a string is a contiguous sequence of characters within that string.
Example 1:

Input:  
s1 = "abcde"  
s2 = "abxyzcde"  

Output:  
3  

Explanation:  
- The longest subsequence of s1 that is a substring of s2 is "cde".  
- "cde" appears contiguously in s2, and it is a subsequence of s1.  
- The length of "cde" is 3.  
Example 2:

Input:  
s1 = "abcdef"  
s2 = "xyzabcpqrs"  

Output:  
3  

Explanation:  
- The longest subsequence of s1 that is a substring of s2 is "abc".  
- The length of "abc" is 3.  
Constraints:

1 ≤ n, m ≤ 10^3
s1 and s2 consist of lowercase English letters only.
'''

def longestCommonSubstring(s1: str, s2: str) -> str:
    if not s1 or not s2:
        return ""
    m, n = len(s1), len(s2)
    dp = [[0] *(n+1) for _ in range(m+1)]
    start, maxlen = 0, 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
                if maxlen < dp[i][j]:
                    maxlen = dp[i][j]
                    start = i - maxlen
    return s1[start: start+maxlen]

# s1 = "abcdef"  
# s2 = "xyzabcpqrs" 
s1 = "abcde"  
s2 = "abxyzcde"  
print(f"{longestCommonSubstring(s1, s2)}")