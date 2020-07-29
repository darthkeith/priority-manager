from math import log10

# Box-drawing characters for drawing tree                                       
BOX_L = '\u255a'        # L
BOX_T = '\u2566'        # T
BOX_TSIDE = '\u2560'    # |-
BOX_VERT = '\u2551'     # |
BOX_DASH = '\u2550'     # -


class Node:
    """Node in comparison heap."""

    def __init__(self, name, left, right):
        if right:
            height = 1 + min(left.height, right.height)
            size = 1 + left.size + right.size 
        else:
            height = 0
            size = 1 + left.size if left else 1
        self.name = name        # name of item
        self.left = left        # left child
        self.right = right      # right child
        self.height = height    # min distance to descendant without two children
        self.size = size        # number of nodes in subtree

    def copy(self, left, right):
        return Node(self.name, left, right)


class ComparisonHeap:
    """
    A Left-leaning binary heap of strings for which operations are performed
    with a minimal number of comparisons.

    filename: If empty string, create new heap, otherwise open saved heap.

    """

    def __init__(self, filename):
        self.root = None
        if not filename:
            return
        def build_heap(f):
            name = f.readline()[:-1]
            if not name:
                return None
            left = build_heap(f)
            right = build_heap(f)
            return Node(name, left, right)
        with open(filename, 'r') as f:
            self.root = build_heap(f)

    def save(self, filename):
        """Save heap to file."""
        def to_string(root):
            if root == None:
                return '\n'
            return root.name + '\n' + to_string(root.left) + to_string(root.right)
        with open(filename, 'w') as f:
            f.write(to_string(self.root))

    def add(self, name, is_higher):
        """Add name to heap."""
        if not name:
            name = ' '
        def leaf(name):
            return Node(name, None, None)
        if self.is_empty():
            self.root = leaf(name)
            return
        def do_add(root):
            if is_higher(name, root.name):
                return Node(name, root, None)
            if root.left == None:
                return root.copy(leaf(name), None)
            if root.right == None:
                return root.copy(root.left, leaf(name))
            if root.right.height < root.left.height:
                right = do_add(root.right)
                return root.copy(root.left, right)
            left = do_add(root.left)
            return root.copy(left, root.right)
        self.root = do_add(self.root)

    def delete(self, idx, is_higher):
        """Delete node at pre-order index and return its name."""
        def merge(x, y):
            # Merge two non-empty subtrees.
            root, child = (x, y) if is_higher(x.name, y.name) else (y, x)
            if root.left == None:
                return root.copy(child, None)
            if root.right == None:
                return root.copy(root.left, child)
            if root.right.height < root.left.height:
                right = merge(root.right, child)
                return root.copy(root.left, right)
            left = merge(root.left, child)
            return root.copy(left, root.right)
        name = ''
        def do_delete(root, current_idx):
            if current_idx == idx:
                nonlocal name
                name = root.name
                if root.right == None:
                    return root.left
                return merge(root.left, root.right)
            left_idx = 1 + current_idx
            right_idx = left_idx + root.left.size
            if idx < right_idx:
                left = do_delete(root.left, left_idx)
                if left == None:
                    return root.copy(root.right, None)
                return root.copy(left, root.right)
            right = do_delete(root.right, right_idx)
            return root.copy(root.left, right)
        self.root = do_delete(self.root, 0)
        return name

    def move(self, idx, is_higher):
        """Delete node at pre-orde index, reinsert it, and return its name."""
        name = self.delete(idx, is_higher)
        self.add(name, is_higher)
        return name

    def rename(self, idx, name):
        """Rename node at pre-order index."""
        if not name:
            name = ' '
        def do_rename(node, current_idx):
            if current_idx == idx:
                node.name = name
                return
            left_idx = 1 + current_idx
            right_idx = left_idx + node.left.size
            if idx < right_idx:
                do_rename(node.left, left_idx)
                return
            do_rename(node.right, right_idx)
        do_rename(self.root, 0)

    def display_tree(self):
        """
        Get list of string 3-tuples representing the rows of the displayed tree.

        Format of each 3-tuple: (index string, tree string, item name)
        """
        if self.is_empty():
            return []
        if self.root.size == 1:
            ndigits = 1
        else:
            ndigits = 1 + int(log10(self.root.size - 1))
        row_list = []
        def build_rows(root, prefix, is_last_child):
            idx_str = "{:>{}}".format(len(row_list), ndigits)
            tree_str = prefix
            if is_last_child:
                tree_str += BOX_L
                prefix += ' '
            else:
                tree_str += BOX_TSIDE
                prefix += BOX_VERT
            is_leaf = root.left == None
            tree_str += BOX_DASH if is_leaf else BOX_T
            row_list.append((idx_str, tree_str, root.name))
            if is_leaf:
                return
            build_rows(root.left, prefix, root.right == None)
            if root.right:
                build_rows(root.right, prefix, True)
        build_rows(self.root, '', True)
        return row_list

    def is_empty(self):
        """Is the heap empty?"""
        return self.root == None

    def is_valid_idx(self, idx):
        """Is this the index of an item in the heap?"""
        if self.is_empty():
            return False
        return idx >= 0 and idx < self.root.size

