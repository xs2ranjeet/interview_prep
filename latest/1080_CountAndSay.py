'''
1080. Count and Say Sequence | String Compression | Word Compression
https://enginebogie.com/interview/experience/salesforce-software-development-engineer/771
Coding and Problem-SolvingData Structures & Algorithms (DSA)StringRecursionCompressionTwo Pointer
Medium
The Count and Say sequence is a series of digit strings defined recursively. The sequence starts with countAndSay(1) = "1". 
For each subsequent number n, countAndSay(n) is derived by performing a run-length encoding of the previous term countAndSay(n - 1).

Run-length encoding is a method of string compression where consecutive identical characters are replaced by 
the concatenation of the character and the number representing the count of the characters. 
For instance, the string "3322251" can be encoded as "23321511":

"33" is replaced by "23"
"222" is replaced by "32"
"5" is replaced by "15"
"1" is replaced by "11"
Given a positive integer n, your task is to return the nth element of the Count and Say sequence.

Example 1:
Input: n = 1
Output: "1"
Explanation: 
- The first sequence is "1".
Example 2:
Input: n = 4
Output: "1211"
Explanation:
- The sequence progresses as follows:
  countAndSay(1) = "1"
  countAndSay(2) = "11" (one 1)
  countAndSay(3) = "21" (two 1s)
  countAndSay(4) = "1211" (one 2, then one 1)
Example 3:
Input: n = 5
Output: "111221"
Explanation:
- The sequence progresses as follows:
  countAndSay(1) = "1"
  countAndSay(2) = "11" (one 1)
  countAndSay(3) = "21" (two 1s)
  countAndSay(4) = "1211" (one 2, then one 1)
  countAndSay(5) = "111221" (one 1, one 2, then two 1s)
'''
def countAndSay(n: int) -> str :
    if n < 0:
        return ""
    if n == 1:
        return "1"
    prev = "1"
    for _ in range(2, n+1):
        result = []
        i = 0
        while i < len(prev):
            j = i
            while j < len(prev) and prev[j] == prev[i]:
                j += 1
            count = j - i
            result.append(str(count))
            result.append(prev[i])
            i = j
        prev = ''.join(result)
    return prev

print(f"{countAndSay(4)}")
print(f"{countAndSay(5)}")
print(f"{countAndSay(6)}")