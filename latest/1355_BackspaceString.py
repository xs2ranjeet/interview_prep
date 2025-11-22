'''
1355. Backspace String Comparison
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/237
Coding and Problem-SolvingStackTwo PointerString ProcessingData Structures & Algorithms (DSA)
Medium
You are given two strings, s1 and s2, which contain lowercase alphabets (a-z) and the # character (which represents a backspace).

A # removes the most recent non-deleted character before it (if any).

Your task is to determine whether s1 and s2 are equal after processing all backspaces.

Example 1:

Input:  
s1 = "ab#c"  
s2 = "ad#c"  

Output:  
True  

Explanation:  
- s1: "ab#c" → "ac"  
- s2: "ad#c" → "ac"  
- Both strings are equal after processing backspaces.
Example 2:

Input:  
s1 = "a##c"  
s2 = "#a#c"  

Output:  
True  

Explanation:  
- s1: "a##c" → "c"  
- s2: "#a#c" → "c"  
- Both strings are equal after processing backspaces.
Example 3:

Input:  
s1 = "abc#d"  
s2 = "acc#c"  

Output:  
False  

Explanation:  
- s1: "abc#d" → "abd"  
- s2: "acc#c" → "acc"  
- The processed strings are not equal.
Constraints:

1 ≤ len(s1), len(s2) ≤ 10^5
s1 and s2 contain only lowercase letters (a-z) and # characters.
'''

def backspaceStringCompareOptimized(s1: str, s2: str) -> bool:
    i, j = len(s1) -1, len(s2) - 1
    skip1, skip2 = 0, 0

    while i >=0 and j >=0:
        # get valid char from s1
        while i >= 0:
            if s1[i] == '#':
                skip1 += 1
            elif skip1 > 0:
                skip1 -= 1
            else:
                break
            i -= 1

        # get valid char from s2
        while j >= 0:
            if s2[j] == '#':
                skip2 += 1
            elif skip2 > 0:
                skip2 -= 1
            else:
                break
            j -= 1
        if i == 0 and j == 0:
            return True
        if i >= 0 and j >= 0 and s1[i] != s2[j]:
            return False
        if (i >= 0) != (j >= 0):
            return False
        i -= 1
        j -= 1

    return True


def backspaceStringCompare(s1: str, s2: str) -> bool :
    
    def removeBackSpace(s: str) -> str:
        if not s:
            return ""
        temp = []
        i = len(s) -1
        backCount = 0
        while i >= 0:
            if s[i] != '#':
                if backCount == 0:
                    temp.append(s[i])
                else:
                    backCount -= 1

            if(s[i] == '#'):
                backCount += 1
            i -= 1
        return ''.join(reversed(temp))
    s1 = removeBackSpace(s1)
    s2 = removeBackSpace(s2)
    print(f"{s1} {s2}")
    return s1 == s2

s1 = "ab#c"  
s2 = "ad#c"  

print(f"{backspaceStringCompareOptimized(s1, s2)}")

s1 = "abc#d"  
s2 = "acc#c"  
print(f"{backspaceStringCompareOptimized(s1, s2)}")

