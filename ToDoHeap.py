"""
This is a command line program that stores items in a left-leaning binary heap
(not necessarily complete) with priority chosen by the user such that the user
is required to make as few comparisons as possible.

To open a saved heap:
python ToDoHeap.py [filename]
"""

from os.path import isfile
from sys import argv
from math import log10
from pathvalidate import is_valid_filename

HELP = """
    peek/<Enter> - Show item of highest priority

    list/ls - Display all items with their indices

    add [name] - Add item with name

    delete/del [index] - Delete item at index (0 by default)

    move/mv [index] - Move item to new position 

    rename/rn [index] [name] - Rename item at index

    quit/q - Save and quit

    help - List available commands"""
EMPTY_HEAP = "Heap is empty."
UNRECOGNIZED = """Command not recognized.
Type "help" for list of available commands."""


class Node:
    """"Node in a binary heap"""

    def __init__(self, item):
        self.item = item  # name of item
        self.left = None  # left child
        self.right = None # right child
        self.height = 0   # minimum distance to descendant without two children
        self.size = 1     # number of nodes in subtree

# Get text representation of heap
def to_text(node):
    if node == None:
        return "\n"
    return node.item + "\n" + to_text(node.left) + to_text(node.right)

# Build heap from open text file
def build_heap(f):
    item = f.readline().strip()
    if not item:
        return None
    node = Node(item)
    node.left = build_heap(f)
    node.right = build_heap(f)
    if node.left == None:
        pass
    elif node.right == None:
        node.size = node.left.size + 1
    else:
        node.height = 1 + min(node.left.height, node.right.height)
        node.size = 1 + node.left.size + node.right.size
    return node

# Helper function to display heap
def display(node, is_last_child, line, digits, prefix):
    print("{:<{}}".format(line, digits) + prefix, end="")
    line += 1
    c = " "
    if is_last_child:
        print("\u255a", end="") # L
    else:
        print("\u2560", end="") # |-
        c = "\u2551"            # |
    if node.left == None:
        print("\u2550" + node.item) # -
    else:
        print("\u2566" + node.item) # T
        prefix += c
        is_last_child = node.right == None
        line = display(node.left, is_last_child, line, digits, prefix)
        if not is_last_child:
            line = display(node.right, True, line, digits, prefix)
    return line

# Is item A of higher priority than item B?
def is_higher(item_A, item_B):
    print("1. " + item_A)
    print("2. " + item_B)
    while True:
        c = input("Higher priority: ")
        if not c:
            continue
        if c == "1":
            return True
        elif c == "2":
            return False

# Add an item to a non-empty subtree
def add(node, item):
    if is_higher(item, node.item):
        x = Node(item)
        x.left = node
        x.size = 1 + node.size
        return x
    if node.left == None:
        node.left = Node(item)
    elif node.right == None:
        node.right = Node(item)
        node.height = 1
    else:
        if node.right.height < node.left.height:
            node.right = add(node.right, item)
        else:
            node.left = add(node.left, item)
        node.height = 1 + min(node.left.height, node.right.height)
    node.size += 1 
    return node

# Merge two non-empty heaps together
def merge(x, y):
    if is_higher(y.item, x.item):
        x, y = y, x
    if x.left == None:
        x.left = y
    elif x.right == None:
        x.right = y
        x.height = 1 + min(x.left.height, y.height)
    else:
        if x.right.height < x.left.height:
            x.right = merge(x.right, y)
        else:
            x.left = merge(x.left, y)
        x.height = 1 + min(x.left.height, x.right.height)
    x.size += y.size
    return x

# Delete node at target index in pre-order traversal and return its item
def delete(node, i, target):
    if i == target:
        if node.right == None:
            return node.left, node.item
        return merge(node.left, node.right), node.item
    if node.right == None:
        node.left, item = delete(node.left, i + 1, target)
    else:
        r = i + node.left.size + 1
        if target < r:
            node.left, item = delete(node.left, i + 1, target)
            if node.left == None:
                node.left = node.right
                node.right = None
        else:
            node.right, item = delete(node.right, r, target)
        if node.right == None:
            node.height = 0
        else:
            node.height = 1 + min(node.left.height, node.right.height)
    node.size -= 1
    return node, item

# Rename node at target index in pre-order traversal
def rename(node, i, target, name):
    if i == target:
        print("Old: " + node.item)
        node.item = name
    elif node.right == None:
        rename(node.left, i + 1, target, name)
    else:
        r = i + node.left.size + 1
        if target < r:
            rename(node.left, i + 1, target, name)
        else:
            rename(node.right, r, target, name)


class ToDoHeap:
    """Left-leaning binary heap"""

    # Construct a heap from a file, or a new heap if filename is empty
    def __init__(self, filename):
        self.root = None
        if filename:
            with open(filename, "r") as f:
                self.root = build_heap(f)

    # Store the current heap as a file so it can be reconstructed
    def save(self, filename):
        with open(filename, "w") as f:
            f.write(to_text(self.root))

    # Print the item at the top of the heap
    def peek(self):
        if self.root:
            print(self.root.item)
        else:
            print(EMPTY_HEAP)

    # Display the heap, showing the index of each item
    def display(self):
        if self.root:
            digits =  1 + int(log10(self.root.size))
            display(self.root, True, 0, digits, "")
        else:
            print(EMPTY_HEAP)

    # Add an item to the heap
    def add(self, item):
        if self.root:
            self.root = add(self.root, item)
        else:
            self.root = Node(item)
        print("Added: " + item)

    # Delete the item at the given index
    def delete(self, i):
        self.root, item = delete(self.root, 0, i)
        print("Deleted: " + item)

    # Delete the item at given index and add it back into the heap
    def move(self, i):
        self.root, item = delete(self.root, 0, i)
        self.add(item)
        print("Moved : " + item)

    # Rename the item at given index
    def rename(self, i, name):
        rename(self.root, 0, i, name)
        print("New: " + name)

    # Is this a valid index in the heap?
    def is_valid_index(self, i):
        if self.root == None:
            print(EMPTY_HEAP)
        elif (i >= 0 and i < self.root.size):
            return True
        else:
            print("Invalid index.")
        return False

# Get the first command line argument if it is a valid file that exists
def get_arg():
    if len(argv) > 1:
        filename = argv[1]
        if not is_valid_filename(filename):
            print("Invalid filename.")
        elif not isfile(filename):
            print("File {} not found.".format(filename))
        else:
            return filename
    return ""

# Parse user input for command and following string
def get_command():
    words = input("\n>>> ").split(None, 1)
    command = ""
    string = ""
    try:
        command = words[0].lower()
        string = words[1]
    except IndexError:
        pass
    return command, string

# Parse string for integer and following string
def get_int(string):
    words = string.split(None, 1)
    i = -1
    string = ""
    try:
        i = int(words[0])
        string = words[1]
    except (IndexError, ValueError):
        pass
    return i, string

# Get a non-empty name
def get_name(name):
    while True:
        name = name.strip()
        if name:
            return name
        name = input("Enter name: ")

# Get a non-empty valid filename
def get_filename():
    while True:
        filename = input("Enter filename: ")
        if is_valid_filename(filename):
            return filename
        print("Invalid filename.")

# Ask if the user wants to save
def save_query():
    while True:
        ans = input("Save heap (y/n)? ") 
        if not ans:
            continue
        c = ans[0].lower()
        if c == "y":
            return True
        elif c == "n":
            return False

if __name__ == "__main__":
    filename = get_arg()
    heap = ToDoHeap(filename)
    heap.peek()
    changed = False
    while True:
        command, string = get_command()
        if command in ("", "peek"):
            heap.peek()
        elif command in ("ls", "list"):
            heap.display()
        elif command == "add":
            name = get_name(string)
            heap.add(name)
            changed = True
        elif command in ("del", "delete"):
            i = get_int(string)[0] if string else 0
            if heap.is_valid_index(i):
                heap.delete(i)
                changed = True
        elif command in ("mv", "move"):
            i = get_int(string)[0]
            if heap.is_valid_index(i):
                heap.move(i)
                changed = True
        elif command in ("rn", "rename"):
            i, string = get_int(string)
            if heap.is_valid_index(i):
                name = get_name(string)
                heap.rename(i, name)
                changed = True
        elif command in ("q", "quit"):
            if changed and save_query():
                if not filename:
                    filename = get_filename()
                heap.save(filename)
            break
        elif command == "help":
            print(HELP)
        else:
            print(UNRECOGNIZED)

