from math import log10

# Box-drawing characters for drawing tree                                       
BOX_L = '\u255a'        # L
BOX_T = '\u2566'        # T
BOX_TSIDE = '\u2560'    # |-
BOX_VERT = '\u2551'     # |
BOX_DASH = '\u2550'     # -


class Node:
    """Node in comparison heap."""

    def __init__(self, name):
        self.name = name    # name of item
        self.left = None    # left child
        self.right = None   # right child
        self.height = 0     # min distance to descendant without two children
        self.size = 1       # number of nodes in subtree

def _build_heap(f):
    # Build heap from open text file and return root node.
    name = f.readline()[:-1]
    if not name:
        return None
    root = Node(name)
    root.left = _build_heap(f)
    root.right = _build_heap(f)
    if root.left == None:
        pass
    elif root.right == None:
        root.size = 1 + root.left.size
    else:
        root.height = 1 + min(root.left.height, root.right.height)
        root.size = 1 + root.left.size + root.right.size
    return root

def _to_string(root):
    # Return string representation of heap for storage.
    if root == None:
        return '\n'
    return root.name + '\n' + _to_string(root.left) + _to_string(root.right)

def _rename(node, idx, target_idx, new_name):
    # Rename node at target pre-order index.
    if idx == target_idx:
        node.name = new_name
    elif node.right == None:
        _rename(node.left, idx + 1, target_idx, new_name)
    else:
        right_idx = idx + node.left.size + 1
        if target_idx < right_idx:
            _rename(node.left, idx + 1, target_idx, new_name)
        else:
            _rename(node.right, right_idx, target_idx, new_name)


class ComparisonHeap:
    """
    A Left-leaning binary heap of strings for which operations are performed
    with a minimal number of comparisons.

    Parameters:
        filename: Name of saved file, or empty string if creating a new heap.

        is_higher: Callback function that compares the priority of two strings.

    """

    def __init__(self, filename, is_higher):
        self.root = None
        self.is_higher = is_higher
        if filename:
            with open(filename, 'r') as f:
                self.root = _build_heap(f)

    def save(self, filename):
        """Save heap to file."""
        with open(filename, 'w') as f:
            f.write(_to_string(self.root))

    def _add(self, root, name):
        # Add name to non-empty subtree.
        if self.is_higher(name, root.name):
            x = Node(name)
            x.left = root
            x.size = 1 + root.size
            return x
        if root.left == None:
            root.left = Node(name)
        elif root.right == None:
            root.right = Node(name)
            root.height = 1
        else:
            if root.right.height < root.left.height:
                root.right = self._add(root.right, name)
            else:
                root.left = self._add(root.left, name)
            root.height = 1 + min(root.left.height, root.right.height)
        root.size += 1 
        return root

    def add(self, name):
        """Add name to heap."""
        if not name:
            name = ' '
        if self.is_empty():
            self.root = Node(name)
        else:
            self.root = self._add(self.root, name)

    def _merge(self, x, y):
        # Merge two non-empty subtrees together.
        if self.is_higher(y.name, x.name):
            root, z = y, x
        else:
            root, z = x, y
        if root.left == None:
            root.left = z
        elif root.right == None:
            root.right = z
            root.height = 1 + min(root.left.height, root.right.height)
        else:
            if root.right.height < root.left.height:
                root.right = self._merge(root.right, z)
            else:
                root.left = self._merge(root.left, z)
            root.height = 1 + min(root.left.height, root.right.height)
        root.size += z.size
        return root

    def _delete(self, root, idx, target_idx):
        # Delete node at target pre-order index and return its name.
        if idx == target_idx:
            if root.right == None:
                return root.left, root.name
            return self._merge(root.left, root.right), root.name
        if root.right == None:
            root.left, name = self._delete(root.left, idx + 1, target_idx)
        else:
            right_idx = idx + root.left.size + 1
            if target_idx < right_idx:
                root.left, name = self._delete(root.left, idx + 1, target_idx)
                if root.left == None:
                    root.left = root.right
                    root.right = None
            else:
                root.right, name = self._delete(root.right, right_idx, target_idx)
            if root.right == None:
                root.height = 0
            else:
                root.height = 1 + min(root.left.height, root.right.height)
        root.size -= 1
        return root, name

    def delete(self, idx):
        """Delete node at pre-order index and return its name."""
        self.root, name = self._delete(self.root, 0, idx)
        return name

    def move(self, idx):
        """Delete node at pre-orde index, reinsert it, and return its name."""
        name = self.delete(idx)
        self.add(name)
        return name

    def rename(self, idx, name):
        """Rename node at pre-order index."""
        if not name:
            name = ' '
        _rename(self.root, 0, idx, name)

    def _max_idx_digits(self):
        # Number of digits in longest index.
        if self.is_empty():
            return 0
        if self.root.size == 1:
            return 1
        return 1 + int(log10(self.root.size - 1))

    def _display_tree(self, root, row_list, prefix, is_last_child, ndigits):
        # Helper function for display_tree method that builds row_list.
        idx_str = "{:>{}}".format(len(row_list), ndigits)
        tree_str = prefix
        if is_last_child:
            tree_str += BOX_L
            prefix += ' '
        else:
            tree_str += BOX_TSIDE
            prefix += BOX_VERT
        is_leaf = root.left == None
        if is_leaf:
            tree_str += BOX_DASH
        else:
            tree_str += BOX_T
        row_list.append((idx_str, tree_str, root.name))
        if is_leaf:
            return
        one_child = root.right == None
        self._display_tree(root.left, row_list, prefix, one_child, ndigits)
        if not one_child:
            self._display_tree(root.right, row_list, prefix, True, ndigits)

    def display_tree(self):
        """
        Get list of string 3-tuples representing the rows of the displayed tree.

        Format of each 3-tuple: (index string, tree string, item name)
        """
        row_list = []
        if self.is_empty():
            return row_list
        self._display_tree(self.root, row_list, '', True, self._max_idx_digits())
        return row_list

    def is_empty(self):
        """Is the heap empty?"""
        return self.root == None

    def is_valid_idx(self, idx):
        """Is this the index of an item in the heap?"""
        if self.is_empty():
            return False
        return idx >= 0 and idx < self.root.size

