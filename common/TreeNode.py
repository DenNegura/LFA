import queue
from typing import Callable, Any


class TreeNode:

    def __init__(self, val: Any = None,
                 parent: 'TreeNode' = None,
                 left: 'TreeNode' = None,
                 right: 'TreeNode' = None,
                 props: dict = None):
        self.parent = parent
        self.val = val
        self.left = left
        self.right = right
        self.props = dict()
        if props:
            self.props = props

    def wide(self, callback: Callable):
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            node = q.get()
            callback(node)
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)

    def preorder(self, callback: Callable):
        def recursion(node: TreeNode):
            if not node:
                return
            callback(node)
            recursion(node.left)
            recursion(node.right)

        recursion(self)

    def postorder(self, callback: Callable):
        def recursion(node: TreeNode):
            if not node:
                return
            recursion(node.left)
            recursion(node.right)
            callback(node)

        recursion(self)
