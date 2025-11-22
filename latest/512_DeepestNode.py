'''
512. Deepest Node in a Complete Binary Tree
https://enginebogie.com/public/question/deepest-node-in-a-complete-binary-tree/512
Medium
You are given a complete binary tree, which is a binary tree where all levels are completely filled except possibly for the last level, which is filled from left to right. Your task is to find and return the deepest node in this complete binary tree.

Input:

A complete binary tree represented in a suitable data structure.
Output:

Return the deepest node in the complete binary tree.
Example:
'''
from collections import deque
from typing import List, Optional

class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    """Builds a binary tree from level-order list (None = empty)."""
    if not arr:
        return None
    
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    
    while q and i < len(arr):
        node = q.popleft()
        
        if arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    
    return root

def countNode(root: TreeNode):
    if not root:
        return 0
    lh ,rh = 0, 0
    leftNode = root
    while leftNode:
        lh += 1
        leftNode = leftNode.left
    rightNode = root
    while rightNode:
        rh += 1
        rightNode = rightNode.right
    if lh == rh:
        return (1 << lh ) -1
    return 1 + countNode(root.left) + countNode(root.right)

def findDepthNodeOfTree(root: TreeNode):
    if not root:
        return -1
    nodes = countNode(root)
    pathbits = bin(nodes)[3:]  # bin return binary repre includinf 0b as prefix. skip the 0b and 1 bit i.e. 0b1...
    # now traverse the tree as per the set bits
    node = root
    for path in pathbits:
        node = node.right if path == '1' else node.left
    return node.val


rootList = [1, 2, 3, 4, 5, 6]
root = buildTree(rootList)
print(f"{findDepthNodeOfTree(root)}")

# Summary Table
# Approach	Time	Space	Use Case
# Array/Heap	O(1)	O(1)	Tree as array/list
# BFS Queue w/ Nodes	O(N)	O(W)	General/unrestricted access
# Linked: Binary Path	O(log^2 N)	O(1)	Only root available, must walk to node