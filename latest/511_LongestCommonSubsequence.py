'''
511. Longest Common Subsequence
https://enginebogie.com/interview/experience/salesforce-software-development-engineer/771
Dynamic Programming (DP)Coding and Problem-SolvingAlgorithmsString Manipulation
Medium
You are given two sequences, often strings or arrays, and your task is to find the longest common subsequence (LCS) between them. 
A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without 
changing the order of the remaining elements. The LCS is the longest subsequence that is common to both sequences.

Input:

Two sequences, which can be strings or arrays.
Output:

Return the longest common subsequence of the given sequences.
Example:

Input: sequence1 = "AGGTAB", sequence2 = "GXTXAYB"
Output: "GTAB"


dp[i][j] = s[i] == s[j] => 1 + dp[i-1][j-1] 
         = not equal = max(dp[i-1][j], dp[i][j-1])


'''

def longestCommonSubsequence1(seq1: str, seq2: str) -> str:
    m, n = len(seq1), len(seq2)
    dp = [[""] * (n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i-1][j-1] + seq1[i-1]
            else:
                if len(dp[i-1][j]) > len(dp[i][j-1]):
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i][j-1]
    return dp[m][n]

def longestCommonSubsequence(seq1: str, seq2: str) -> str:
    if not seq1 or not seq2:
        return ""
    m, n = len(seq1), len(seq2)
    dp = [[0] *(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    output = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i-1] == seq2[j-1]:
            output.append(seq1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    output.reverse()
    return ''.join(output)



sequence1 = "AGGTAB"
sequence2 = "GXTXAYB"

print(f"{longestCommonSubsequence1(sequence1, sequence2)}")

print(f"{longestCommonSubsequence(sequence1, sequence2)}")
