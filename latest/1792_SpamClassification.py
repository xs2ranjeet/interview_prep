'''
1792. Spam Classification Based on Word Matching
https://enginebogie.com/interview/experience/salesforce-software-engineer/696
Coding and Problem-SolvingData Structures & Algorithms (DSA)StringHashingString Processing
Medium
Build a simple classification system to detect whether a given text should be marked as "spam" or "not_spam". 
The system uses a predefined list of spam words.

A text is labeled as "spam" if it contains at least two occurrences of spam words.

Matching is case-sensitive.
Each occurrence of a spam word counts separately toward the total.
Return a list of labels ("spam" or "not_spam") for the given set of texts.

Example 1:
Input:
texts = [
    "This is a limited offer just for you",
    "Win cash now! Click here to claim your prize",
    "Hello friend, just checking in",
    "Congratulations! You have won a free gift"
]

spamWords = [
    "offer", "cash", "Click", "prize", "Congratulations", "free"
]

Output:
["not_spam", "spam", "not_spam", "spam"]

Explanation:
1. "This is a limited offer just for you"
   → Contains "offer" (1 spam word) → not_spam
2. "Win cash now! Click here to claim your prize"
   → Contains "cash", "Click", "prize" (3 spam words) → spam
3. "Hello friend, just checking in"
   → Contains 0 spam words → not_spam
4. "Congratulations! You have won a free gift"
   → Contains "Congratulations", "free" (2 spam words) → spam
Example 2:
Input:
texts = [
    "offer offer offer",
    "Click cash Click"
]

spamWords = [
    "offer", "cash", "Click"
]

Output:
["spam", "spam"]

Explanation:
1. "offer offer offer"
   → Contains "offer" 3 times → spam
2. "Click cash Click"
   → Contains "Click" twice and "cash" once (total 3) → spam
Constraints:

1 ≤ n ≤ 10^3 (number of texts)
1 ≤ k ≤ 10^5 (number of spam words)
1 ≤ len(text) ≤ 10^5
1 ≤ len(spamWord) ≤ 10^5
Combined length of all spam words ≤ 10^7
'''

from typing import List

texts = [
    "This is a limited offer just for you",
    "Win cash now! Click here to claim your prize",
    "Hello friend, just checking in",
    "Congratulations! You have won a free gift"
]

spamWords = [
    "offer", "cash", "Click", "prize", "Congratulations", "free"
]

texts2 = [
    "offer offer offer",
    "Click cash Click"
]

spamWords2 = [
    "offer", "cash", "Click"
]

# Output:
# ["not_spam", "spam", "not_spam", "spam"]

def classifyText(texts:List[str], spamWords:List[str]) -> List[str]:
    spamSet = set(spamWords)
    output = []
    for text in texts:
        spamWordCount = 0
        for spam in spamSet:
            occurence = text.count(spam)
            spamWordCount += occurence
            if spamWordCount >= 2:
                output.append("spam")
                break
        if spamWordCount < 2:
            output.append("not_spam")
    return output

def classifyText2(texts:List[str], spamWords:List[str]) -> List[str]:
    spamSet = set(spamWords)
    output = []
    for text in texts:
        spamWordCount = 0
        words = text.split()
        for word in words:
            if word in spamSet:
                spamWordCount += 1
            if spamWordCount >= 2:
                output.append("spam")
                break
        if spamWordCount < 2:
            output.append("not_spam")
    return output

print(f"{classifyText2(texts, spamWords)}")
print(f"{classifyText2(texts2, spamWords2)}")