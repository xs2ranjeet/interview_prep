'''
288. Auto-Complete Feature using Tries | Implementing Search Queries Using Trie
https://enginebogie.com/public/question/auto-complete-feature-using-tries-implementing-search-queries-using-trie/288
Medium
Design and implement a system that efficiently processes search queries by utilizing a Trie (prefix tree) data structure. The system should support the following functionalities:

Insertion of Words: Add words to the Trie to build the search index.

Search for Exact Matches: Check if a given word exists in the Trie.

Autocomplete Suggestions: Given a prefix, retrieve all words in the Trie that start with that prefix.

Partial Match Queries with Wildcards: Support search queries that include wildcards (e.g., '?') representing any single character, returning all words that match the pattern.

Example 1:

Input:
Set of words: ["apple", "application", "apply", "art", "artist", "ball", "bat", "batman"]

Output:
Trie:
        - a -
       /     \
      p       r
     /         \
    p           t
   /             \
  l               i
 /  \              \
e    i              s
       \           /
        c.        t
         \
          a   
         /     
        t      
       /      
      i       
     /        
    o        
   /          
  n          

Auto-Complete Suggestions for Prefix "ap":
- apple
- application
- apply

Auto-Complete Suggestions for Prefix "ba":
- ball
- bat
- batman
Note:

The trie data structure should be efficiently constructed to store the words.
The auto-complete feature should provide suggestions based on the given prefix.
The suggestions should be sorted in lexicographic order.
The trie should support lowercase alphabets (a-z) and can include special characters or numbers if required.
The auto-complete feature should handle edge cases such as an empty prefix or no suggestions available for a given prefix.
'''