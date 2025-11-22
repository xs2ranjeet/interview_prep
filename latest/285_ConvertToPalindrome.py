'''
285. Convert to Palindrome
Medium
Given a string, your task is to determine if it is possible to convert the string into a palindrome by removing 
exactly one character. Return true if it is possible, and false otherwise.

A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward.

Furthermore, extend your solution to handle the cases where you can remove exactly two characters or k characters 
(k being a positive integer) to convert the string into a palindrome.

Example 1:

Input: s = "racecar"
Output: true
Explanation: The string is already a palindrome, so it is possible to convert it to a palindrome by removing one character (middle 'e').
Example 2:

Input: s = "abca"
Output: true
Explanation: By removing 'b' or 'c', the string can be converted to the palindrome "aca".
Example 3:

Input: s = "abcda"
Output: false
Explanation: No single character removal can make the string a palindrome.
Follow-up:

Extend the solution to handle cases where you can remove exactly two characters to convert the string into a palindrome.
Further extend the solution to handle cases where you can remove k characters (k being a positive integer) to convert the string into a palindrome.
'''

def canBePalindromeByRemovingK(s: str, k: int) -> bool:
    n = len(s)
    dp = [[0]*n for _ in range(n)]

    # Length 1 palindromes
    for i in range(n):
        dp[i][i] = 1

    # LPS DP bottom-up
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if i+1 <= j-1 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    lps = dp[0][n-1]
    needed_removals = n - lps

    return needed_removals <= k
