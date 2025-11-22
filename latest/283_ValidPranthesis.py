'''
https://enginebogie.com/public/question/valid-parenthesis-string-validate-parentheses/283
283. Valid Parenthesis String | Validate Parentheses
Medium
Given a string containing only the characters '(' , ')' , and '*' , determine if the string is valid. The validity of a string is defined by the following rules:

Any left parenthesis '(' must have a corresponding right parenthesis ')' at some index to its right.
Any right parenthesis ')' must have a corresponding left parenthesis '(' at some index to its left.
The '*' character can represent either a left parenthesis '(' , a right parenthesis ')' , or an empty string.
Design an algorithm to check the validity of a given parenthesis string. Return true if the string is valid, and false otherwise.

Examples:

1. Input: s = "()"
   Output: true
   Explanation: The string contains a valid pair of parentheses.

2. Input: s = "(*)"
   Output: true
   Explanation: The '*' can be treated as an empty string, making the string valid.

3. Input: s = "(*))"
   Output: true
   Explanation: The '*' can be treated as a left parenthesis '(', making the string valid.

4. Input: s = "((*)"
   Output: true
   Explanation: The '*' can be treated as a right parenthesis ')', making the string valid.

5. Input: s = "((())"
   Output: false
   Explanation: The string does not have a valid closing parenthesis for the opening parenthesis at index 2.

Note:
In the given examples, the strings are evaluated according to the validity rules. 
The '*' character can be interpreted as a left parenthesis, right parenthesis, or an empty string to make the string valid.
'''

def checkValidString(s: str) -> bool:
    minOpen = 0     # minimum '(' possible
    maxOpen = 0     # maximum '(' possible
    for ch in s:
        if ch == "(":
            minOpen += 1
            maxOpen += 1
        elif ch ==")":
            minOpen -= 1
            maxOpen -= 1
        else:
            minOpen -= 1
            maxOpen += 1

        if maxOpen < 0:
            return False  # too many open
        if minOpen < 0:
            return False
    return minOpen == 0