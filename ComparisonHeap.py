#!/usr/bin/env python3

"""
This is a command line program that stores items in a left-leaning binary heap
with priority chosen by the user such that the user is required to make as few
comparisons as possible.

To open a saved heap:
./ComparisonHeap.py filename
"""

from sys import argv, path
from os.path import isfile, join
from configparser import ConfigParser
from math import log10

# Fix colors on Windows
from os import name as OS_NAME
if OS_NAME == 'nt':
    try:
        from colorama import init 
        init()
    except ModuleNotFoundError:
        print("Program may not be displayed correctly.")

COLOR_FILE = "colors.ini"

# Default colors
BACKGROUND0_COLOR = '\x1b[40m'
BACKGROUND1_COLOR = '\x1b[100m'
INDEX_COLOR = '\x1b[32m'
TREE_COLOR = '\x1b[31m'
TEXT_COLOR = '\x1b[37m'

# Other ANSI sequences for colors
RESET = '\x1b[0m'
TO_END = '\x1b[K'

# Box-drawing characters for drawing tree
BOX_L = '\u255a'    # L
BOX_t = '\u2560'    # |-
BOX_VERT = '\u2551' # |
BOX_DASH = '\u2550' # -
BOX_T = '\u2566'    # T

HELP = """
    add NAME        Add item with NAME

    del INDEX       Delete item at INDEX

    mv INDEX        Move item at INDEX

    rn INDEX NAME   Rename item at INDEX with NAME

    q               Save and quit"""
EMPTY_HEAP = "Heap is empty."
UNRECOGNIZED = """Command not recognized.
Type "help" for list of available commands."""

def load_colors():
    color_path = join(path[0], COLOR_FILE)
    global BACKGROUND0_COLOR
    global BACKGROUND1_COLOR
    global INDEX_COLOR
    global TREE_COLOR
    global TEXT_COLOR
    if isfile(color_path):
        config = ConfigParser()
        config.read(color_path)
        colors = config['colors']
        BACKGROUND0_COLOR = colors['background0']
        BACKGROUND1_COLOR = colors['background1']
        INDEX_COLOR = colors['index']
        TREE_COLOR = colors['tree']
        TEXT_COLOR = colors['text']
        return
    colors = {}
    colors['background0'] = BACKGROUND0_COLOR
    colors['background1'] = BACKGROUND1_COLOR
    colors['index'] = INDEX_COLOR
    colors['tree'] = TREE_COLOR
    colors['text'] = TEXT_COLOR
    config = ConfigParser()
    config['colors'] = colors
    with open(color_path, 'w') as f:
        config.write(f)


class Node:
    """"Node in a binary heap"""

    def __init__(self, item):
        self.item = item    # name of item
        self.left = None    # left child
        self.right = None   # right child
        self.height = 0     # min distance to descendant without two children
        self.size = 1       # number of nodes in subtree

# String representation of heap for storage
def to_string(node):
    if node == None:
        return '\n'
    return node.item + '\n' + to_string(node.left) + to_string(node.right)

# Build heap from open text file and return root node
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

# Helper display function
def display(node, is_last_child, line, digits, prefix):
    if (line & 1) == 0:
        print(BACKGROUND0_COLOR, end='')
    else:
        print(BACKGROUND1_COLOR, end='')
    print(INDEX_COLOR + "{:<{}}".format(line, digits) +
          TREE_COLOR + prefix, end='')
    line += 1
    c = ' '
    if is_last_child:
        print(BOX_L, end='')
    else:
        print(BOX_t, end='')
        c = BOX_VERT
    if node.left == None:
        print(BOX_DASH + TEXT_COLOR + node.item + TO_END)
    else:
        print(BOX_T + TEXT_COLOR + node.item + TO_END)
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
        if c == '1':
            return True
        elif c == '2':
            return False

# Add item to non-empty subtree
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


class ComparisonHeap:
    """Left-leaning binary heap for comparing items"""

    def __init__(self, filename):
        self.root = None
        if filename:
            with open(filename, 'r') as f:
                self.root = build_heap(f)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(to_string(self.root))

    def peek(self):
        if self.root:
            print(self.root.item)
        else:
            print(EMPTY_HEAP)

    def display(self):
        if self.root:
            digits =  1 + int(log10(self.root.size))
            display(self.root, True, 0, digits, '')
            print(RESET, end='')
        else:
            print(EMPTY_HEAP)

    def add(self, item):
        if self.root:
            self.root = add(self.root, item)
        else:
            self.root = Node(item)
        print("Added: " + item)

    def delete(self, i):
        self.root, item = delete(self.root, 0, i)
        print("Deleted: " + item)

    def move(self, i):
        self.root, item = delete(self.root, 0, i)
        if self.root:
            self.root = add(self.root, item)
        else:
            self.root = Node(item)
        print("Moved: " + item)

    def rename(self, i, name):
        rename(self.root, 0, i, name)
        print("New: " + name)

    def is_valid_index(self, i):
        if self.root == None:
            print(EMPTY_HEAP)
        elif (i >= 0 and i < self.root.size):
            return True
        else:
            print("Invalid index.")
        return False

# Parse argument following program name for name of existing file
def parse_filename():
    if len(argv) > 1:
        filename = argv[1]
        if isfile(filename):
            return filename
        else:
            print("File {} not found.".format(filename))
    return ''

# Parse first word of user input for command
def parse_command():
    args = input("\n>>> ").split(None, 1)
    command = ''
    rest = ''
    if len(args) > 0:
        command = args[0]
    if len(args) > 1:
        rest = args[1]
    return command, rest

# Parse first word of string for integer
def parse_int(string):
    args = string.split(None, 1)
    i = -1
    rest = ''
    try:
        i = int(args[0])
        string = args[1]
    except (IndexError, ValueError):
        pass
    return i, rest

def save_heap(heap, filename):
    if filename:
        heap.save(filename)
        return
    while True:
        filename = input("Enter filename: ")
        try:
            heap.save(filename)
            return
        except FileNotFoundError:
            pass

def is_save_requested():
    while True:
        ans = input("Save heap (y/n)? ") 
        if not ans:
            continue
        c = ans[0].lower()
        if c == 'y':
            return True
        elif c == 'n':
            return False

if __name__ == "__main__":
    load_colors()
    filename = parse_filename()
    heap = ComparisonHeap(filename)
    changed = False
    while True:
        heap.display()
        command, rest = parse_command()
        if command == 'add':
            if rest:
                heap.add(rest)
                changed = True
        elif command == 'del':
            i = parse_int(rest)[0]
            if heap.is_valid_index(i):
                heap.delete(i)
                changed = True
        elif command == 'mv':
            i = parse_int(rest)[0]
            if heap.is_valid_index(i):
                heap.move(i)
                changed = True
        elif command == 'rn':
            i, name = parse_int(rest)
            if name and heap.is_valid_index(i):
                heap.rename(i, name)
                changed = True
        elif command == 'q':
            if changed and is_save_requested():
                save_heap(heap, filename)
            break
        elif command == 'help':
            print(HELP)
        elif command:
            print(UNRECOGNIZED)

