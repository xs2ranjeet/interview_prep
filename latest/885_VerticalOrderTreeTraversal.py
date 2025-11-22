'''
885. Vertical Order Traversal of a Binary Tree
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/381
Coding and Problem-SolvingData Structures & Algorithms (DSA)Binary TreesTree TraversalTreesBreadth-First Search (BFS)Depth-First Search (DFS)
Medium
Given the root of a binary tree, perform a vertical order traversal from the leftmost level to the rightmost level. In the vertical order traversal, nodes that lie on the same vertical line should be returned in the order of their level from top to bottom as they appear in the tree's level order traversal.

For nodes that share both the same vertical position and the same depth, they should be processed from left to right.

Example 1:

Input: root = [3, 9, 20, null, null, 15, 7]
Output: [[9], [3, 15], [20], [7]]

Explanation:
The tree structure is as follows:

Here, the vertical order traversal from left to right is as follows:
- Column -1: [9]
- Column  0: [3, 15]
- Column  1: [20]
- Column  2: [7]
Example 2:

Input: root = [1, 2, 3, 4, 5, 6, 7]
Output: [[4], [2], [1, 5, 6], [3], [7]]

Explanation:
The tree structure is as follows:

The vertical order traversal is:
- Column -2: [4]
- Column -1: [2]
- Column  0: [1, 5, 6]
- Column  1: [3]
- Column  2: [7]
Constraints:

The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100
'''

from collections import OrderedDict, deque, defaultdict
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


def verticalTreeTraversal(root: TreeNode):
    if not root:
        return []
    col_map  = defaultdict(list)
    bfs = deque()
    bfs.append((root, 0))

    while bfs:
        curr, pos = bfs.popleft()
        col_map[pos].append(curr.val)
        if curr.left:
            bfs.append((curr.left, pos -1))
        if curr.right:
            bfs.append((curr.right, pos+1))

    # result = [value for _, value in sorted(col_map.items(), key=lambda x: x[0])]
    # for key, value in map.items():
        # result.append(value)
    result = [col_map[c] for c in sorted(col_map) ]
    return result


rootList = [1, 2, 3, 4, 5, 6, 7]
root = buildTree(rootList)
output = verticalTreeTraversal(root)
print(output)
#Output: [[4], [2], [1, 5, 6], [3], [7]]