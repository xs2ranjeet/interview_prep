'''
2765. Sequence Building Problem using Backtracking" as asked in the Salesforce Senior Member of Technical Staff interview:

Problem Statement:
Design and implement a solution to generate or validate sequences based on a set of given constraints. 
The problem requires a backtracking approach to explore all possible valid sequences, with a particular emphasis on handling 
various edge cases effectively.

Test Case 1:
Input: Constraints that allow all permutations (n=3)
Expected Output: All possible sequences (e.g., [1,2,3], [1,3,2], etc.)

Test Case 2:
Input: Constraints that exclude certain elements at certain positions (e.g., '2' cannot be at index 1)
Expected Output: Only sequences that fulfill this rule

Test Case 3:
Input: Empty constraints (n=0)
Expected Output: []

Test Case 4:
Input: Sequence has to be ascending
Expected Output: Only ascending sequences

Test Case 5:
Input: Constraints that mutually exclude options (no duplicates)
Expected Output: Only unique sequences

Test Case 6:
Input: Large 'n' where sequence length is high and constraints make many paths invalid
Expected Output: All valid sequences, should handle pruning early

'''