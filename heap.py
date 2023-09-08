"""Module to order and display strings in a heap.

Functions
---------
init(is_higher: CompareStr, preorder: Iterator[str] = iter(['']))
    Initialize the heap.
to_preorder() -> Iterator[str]
    Return the pre-order sequence of strings in the heap.
insert(key: str)
    Insert key into heap.
delete(idx: int) -> str
    Delete node with given pre-order index and return its key.
move(idx: int) -> str
    Delete then reinsert key of node with given pre-order index.
rename(idx: int, name: str)
    Rename item with given pre-order index.
is_empty() -> bool
    Check if heap is empty.
is_valid_idx(idx: int) -> bool
    Check if number is a valid pre-order index.
display() -> Iterator[str]
    Return the strings used to visually display the heap.

Notes
-----
Implements a pairing heap as a child-sibling binary tree.
"""

from typing import Callable, Optional, Iterator

# Type Aliases
CompareStr =  Callable[[str, str], bool]
MaybeNode = Optional['_Node']

# Global Variables
_is_higher: CompareStr = None
_root: '_Node' = None


class _Node:
    """Node in a pairing heap.
    
    Attributes
    ----------
    key : str
        Key used for comparison, assumed to be non-empty.
    child : MaybeNode
        First child.
    sibling : MaybeNode
        Next sibling.
    size : int
        Number of nodes in child-sibling subtree.
    
    Notes
    -----
    Null nodes are represented by a value of `None`.
    """

    def __init__(self,
                 key: str,
                 child: MaybeNode = None,
                 sibling: MaybeNode = None):
        # Construct node with given key, first child, and next sibling.
        self.key = key
        self.child = child
        self.sibling = sibling
        self.size = 1
        self.size += child.size if child else 0
        self.size += sibling.size if sibling else 0

    def with_sibling(self, sibling: MaybeNode) -> '_Node':
        # Return a copy of the node with the given next sibling.
        return _Node(self.key, self.child, sibling)


def init(is_higher: CompareStr,
         preorder: Iterator[str] = iter([''])):
    """Initialize the heap.

    Must be called before the other functions in the module are used.

    Parameters
    ----------
    is_higher : CompareStr
        Callback function used to order strings indicating whether the first
        string has a higher priority than the second.
    preorder : MaybeIterStr, default=iter([''])
        A pre-order sequence of strings, where an empty string represents
        a null node.
    """
    global _is_higher
    global _root
    _is_higher = is_higher
    def build_heap() -> MaybeNode:
        key = next(preorder)
        if key == '':
            return None
        child = build_heap()
        sibling = build_heap()
        return _Node(key, child, sibling)
    _root = build_heap()


def to_preorder() -> Iterator[str]:
    """Return the pre-order sequence of strings in the heap.

    Each null node is represented by an empty string.
    """
    def preorder(node: MaybeNode) -> Iterator[str]:
        if node == None:
            yield ''
            return
        yield node.key
        for k in preorder(node.child):
            yield k
        for k in preorder(node.sibling):
            yield k
    return preorder(_root)


def _merge_pair(x: _Node, y: _Node) -> _Node:
    # Merge two heaps and return the new root (discard sibling references).
    parent, child = (y, x) if _is_higher(y.key, x.key) else (x, y)
    new_child = child.with_sibling(parent.child)
    return _Node(parent.key, new_child, None)


def insert(key: str):
    """Insert key into heap."""
    global _root
    if _root:
        _root = _merge_pair(_root, _Node(key))
    else:
        _root = _Node(key)


def _pair_siblings(node: MaybeNode) -> MaybeNode:
    # Merge siblings pairwise.
    if node == None or node.sibling == None:
        return node
    sibling = node.sibling.sibling
    new_node =_merge_pair(node, node.sibling)
    return new_node.with_sibling(_pair_siblings(sibling))


def _merge_siblings(node: _Node) -> _Node:
    # Recursively merge siblings pairwise into a single heap.
    if node.sibling == None:
        return node
    return _merge_siblings(_pair_siblings(node))


def _concat_siblings(left: MaybeNode, right: MaybeNode) -> MaybeNode:
    # Concatenate two sibling lists.
    if left == None:
        return right
    sibling = _concat_siblings(left.sibling, right)
    return left.with_sibling(sibling)


def delete(idx: int) -> str:
    """Delete node with given pre-order index and return its key."""
    global _root
    if idx == 0:
        key = _root.key
        _root = _merge_siblings(_root.child) if _root.child else None
        return key
    key = ''
    def do_delete(idx: int, node: _Node) -> MaybeNode:
        # Delete node at pre-order index in subtree and return new root.
        if idx == 0:
            nonlocal key
            key = node.key
            return _concat_siblings(node.child, node.sibling)
        right_idx = 1 + (node.child.size if node.child else 0)
        if idx < right_idx:
            child = do_delete(idx - 1, node.child)
            return _Node(node.key, child, node.sibling)
        else:
            sibling = do_delete(idx - right_idx, node.sibling)
            return node.with_sibling(sibling)
    _root = do_delete(idx, _root)
    return key


def move(idx: int) -> str:
    """Delete then reinsert key of node with given pre-order index.

    Return key of target node.
    """
    key = delete(idx)
    insert(key)
    return key


def rename(idx: int, name: str):
    """Rename item with given pre-order index."""
    def do_rename(idx: int, node: _Node):
        if idx == 0:
            node.key = name
            return
        right_idx = 1 + (node.child.size if node.child else 0)
        if idx < right_idx:
            do_rename(idx - 1, node.child)
        else:
            do_rename(idx - right_idx, node.sibling)
    do_rename(idx, _root)


def is_empty() -> bool:
    """Check if heap is empty."""
    return _root == None


def is_valid_idx(idx: int) -> bool:
    """Check if number is a valid pre-order index."""
    if is_empty():
        return False
    return idx >= 0 and idx < _root.size


def display() -> Iterator[str]:
    """Return the strings used to visually display the heap."""
    if is_empty():
        return iter([])
    num_digits = len(str(_root.size - 1))
    idx = 0
    def do_display(node: MaybeNode, prefix: str) -> Iterator[str]:
        if node == None:
            return
        nonlocal idx
        idx_str = f"{idx:>{num_digits}}"
        idx += 1
        c2 = '╦' if node.child else '═'
        if node.sibling:
            c1 = '╠'
            c0 = '║'
        else:
            c1 = '╚'
            c0 = ' '
        yield idx_str + prefix + c1 + c2 + node.key
        for row in do_display(node.child, prefix + c0):
            yield row
        for row in do_display(node.sibling, prefix):
            yield row
    return do_display(_root, '')

