"""Module to order and display strings in a heap.

Functions
---------
init
    Initialize the heap.
to_preorder
    Generate the pre-order sequence of strings in the heap.
insert
    Insert key into heap.
delete
    Delete node with given pre-order index and return its key.
move
    Delete and then reinsert key of node with given pre-order index.
rename
    Rename item with given pre-order index.
is_empty
    Check if heap is empty.
is_valid_index
    Check if number is a valid pre-order index.
display
    Return list of rows of the visual display of the heap.

Notes
-----
Implements a height-biased leftist heap.
"""

from math import log10


class _Node:
    """Node in a height-biased leftist heap.
    
    Attributes
    ----------
    key : str
        Key used for comparison.
    left : _Node
        Left child.
    right : _Node
        Right child.
    rank : int
        Minimum distance to null descendant.
    size : int
        Number of nodes in subtree.
    
    Notes
    -----
    After construction, the right child of a node has a rank no bigger
    than that of its left child (a null node has a rank of zero).
    Null nodes are represented by a value of `None`.
    """

    def __init__(self, key, left, right):
        # Construct node with given key and children.
        if right and left:
            if left.rank < right.rank:
                left, right = right, left
            rank = 1 + right.rank
            size = 1 + left.size + right.size 
        else:
            if right:
                left, right = right, left
            rank = 1
            size = 1 + left.size if left else 1
        self.key = key
        self.left = left
        self.right = right
        self.rank = rank
        self.size = size

    def copy(self, left, right):
        # Construct new node with same key and given children.
        return _Node(self.key, left, right)


def init(is_higher, preorder=None):
    """Initialize the heap.

    Must be called before the other functions in the module are used.

    Parameters
    ----------
    is_higher : function
        Callback function used to order strings: is_higher(x, y) returns
        True when `x` has a higher priority than `y`.
    preorder : iterator of str, default=None
        A pre-order sequence of strings, where an empty string represents
        a null node (the default is None, which indicates an empty heap).
    """
    global _is_higher
    _is_higher = is_higher
    def make_heap():
        key = next(preorder)
        if key == '':
            return None
        left = make_heap()
        right = make_heap()
        return _Node(key, left, right)
    global _root
    _root = make_heap() if preorder else None


def to_preorder():
    """Generate the pre-order sequence of strings in the heap.

    Returns
    -------
    generator of str
        The pre-order sequence of strings in the heap, where each null
        node is represented by an empty string.  To prevent conflict, if
        a node has an empty string as its key, a single space character
        is used instead.
    """
    def key_gen(node):
        if node == None:
            yield ''
            return
        yield ' ' if node.key == '' else node.key
        for k in key_gen(node.left):
            yield k
        for k in key_gen(node.right):
            yield k
    return key_gen(_root)


def insert(key):
    """Insert key into heap."""
    def do_insert(node):
        # Insert key into subtree and return new root.
        if node == None:
            return _Node(key, None, None)
        if _is_higher(key, node.key):
            return _Node(key, node, None)
        right = do_insert(node.right)
        return node.copy(node.left, right)
    global _root
    _root = do_insert(_root)


def delete(idx):
    """Delete node with given pre-order index and return its key."""
    def merge(x, y):
        # Merge two non-empty subtrees.
        parent, child = (y, x) if _is_higher(y.key, x.key) else (x, y)
        if parent.right == None:
            return parent.copy(parent.left, child)
        right = merge(parent.right, child)
        return parent.copy(parent.left, right)
    key = None
    def do_delete(node, curr_idx):
        # Perform deletion from current node/index, return new root.
        if curr_idx == idx:
            nonlocal key
            key = node.key
            if node.right == None:
                return node.left
            return merge(node.left, node.right)
        left_idx = 1 + curr_idx
        right_idx = left_idx + node.left.size
        if idx < right_idx:
            left = do_delete(node.left, left_idx)
            return node.copy(left, node.right)
        right = do_delete(node.right, right_idx)
        return node.copy(node.left, right)
    global _root
    _root = do_delete(_root, 0)
    return key


def move(idx):
    """Delete and then reinsert key of node with given pre-order index.

    Returns
    -------
    key : str
        Key of target node.
    """
    key = delete(idx)
    insert(key)
    return key


def rename(idx, name):
    """Rename item with given pre-order index."""
    def do_rename(node, curr_idx):
        # Perform rename from current node/index.
        if curr_idx == idx: 
            node.key = name
            return
        left_idx = 1 + curr_idx
        right_idx = left_idx + node.left.size
        if idx < right_idx:
            do_rename(node.left, left_idx)
        else:
            do_rename(node.right, right_idx)
    do_rename(_root, 0)


def is_empty():
    """Check if heap is empty."""
    return _root == None


def is_valid_idx(idx):
    """Check if number is a valid pre-order index."""
    if is_empty():
        return False
    return idx >= 0 and idx < _root.size


def display():
    """Return list of rows of the visual display of the heap.

    Returns
    -------
    list of str
        List of rows of the text-based visual display of the heap.
    """
    if is_empty():
        return []
    if _root.size == 1:
        ndigits = 1
    else:
        ndigits = 1 + int(log10(_root.size - 1))
    row_list = []
    def build_rows(node, prefix, is_last_child):
        """Construct rows to add to `row_list`.

        Parameters
        ----------
        node : _Node
            Current node.
        prefix : str
            String used to draw the tree structure on the next row.
        is_last_child : bool
            True if node is a right child or an only child.
        """
        idx_str = "{:>{}}".format(len(row_list), ndigits)
        tree_str = prefix
        if is_last_child:
            tree_str += '╚'
            prefix += ' '
        else:
            tree_str += '╠'
            prefix += '║'
        is_leaf = node.left == None
        tree_str += '═' if is_leaf else '╦'
        row_list.append(idx_str + tree_str + node.key)
        if is_leaf:
            return
        build_rows(node.left, prefix, node.right == None)
        if node.right:
            build_rows(node.right, prefix, True)
    build_rows(_root, '', True)
    return row_list

