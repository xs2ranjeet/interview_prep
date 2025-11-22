'''
2642. Generate All Possible Full Binary Trees
https://enginebogie.com/interview/experience/salesforce-software-engineer/676
Coding and Problem-SolvingData Structures & Algorithms (DSA)TreesBinary TreesDynamic Programming (DP)RecursionCombinatorics
Medium
Given an odd integer n, return every possible full binary tree that contains exactly n nodes. Every node in the tree must have a value of 0. A full binary tree is defined as a tree where each node has either zero or two children.

Input Format:
A single integer n representing the number of nodes.
Output Format:
A list containing the root nodes of all distinct full binary trees. The order of the trees in the list does not matter.
Example 1:
Input:
1

Output:
[TreeNode(0)]
Explanation With only one node the only possible full binary tree consists of that single node.

Example 2:
Input:
3

Output:
[TreeNode(0, left=TreeNode(0), right=TreeNode(0))]
Explanation For three nodes the root must have two children and each child is a leaf. This is the only full binary tree with three nodes.

Constraints:
1 ≤ n ≤ 20
n is odd
'''
from typing import List, Optional
from collections import defaultdict

class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
    
    # def __repr__(self):
    #     print(self.val)

def allPossibleFBTOptimized(n) -> List[Optional[TreeNode]]:
    memo = defaultdict(list)
    def helper(n):
        if n in memo:
            return memo[n]
        if n == 1:
            memo[1] = [TreeNode(0)]
            return memo[1]
        elif n % 2 == 0: # no tree for even node
            memo[n] = 0
            return memo[n]
        
        trees = []
        for i in range(1, n, 2):
            leftNodes = helper(i)
            rightNodes = helper(n-1-i)
            for left in leftNodes:
                for right in rightNodes:
                    trees.append(TreeNode(0, left, right))
        memo[n] = trees
        return trees
    return helper(n)


def allPossibleFBT(n) -> List[Optional [TreeNode]]:

    memo = {}
    res = []
    def helper(n):
        if n % 2 == 0:
            return []  ## for even num, no tree
        if n == 1:
            return [TreeNode(0)]  # for one, there is only one treenode
        if n in memo:
            return memo[n]
        ans = []
        for i in range(1, n, 2):
            leftNodes = helper(i)
            rightNodes = helper(n-1-i)

            for left in leftNodes:
                for right in rightNodes:
                    ans.append(TreeNode(0, left, right))
        memo[n] = ans
        return ans
        
    return helper(n)



print(f"{allPossibleFBTOptimized(3)}")
print(f"{allPossibleFBTOptimized(7)}")