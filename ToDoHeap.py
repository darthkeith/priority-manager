"""
This is a command line program that stores items in a binary heap with priority
chosen by the user such that the user makes as few comparisons as possible.

To start a new heap:
python ToDoHeap.py

To open a saved heap:
python ToDoHeap.py [filename]

A heap can be saved when quitting.  If saving a new heap, a file will be
created with the ".heap" extension.
"""

import os
from sys import argv
from math import log10
from pathvalidate import is_valid_filename

HELP = """
Available commands:

    peek OR <Enter> - Show the item of highest priority

    list OR ls - Display all items

    add [name] - Add item with given name

    delete OR del [index] - Delete the item at index (0 by default)

    reorder OR ro [index] - Reorder the item at index 

    rename OR rn [index] [name] - Rename the item at index

    quit OR q - Save and quit the program

    help - List available commands"""
EMPTY_HEAP = "Heap is empty."
UNRECOGNIZED = """Command not recognized.
Type "help" for list of available commands."""

class Item:
    """"An item in a heap that stores its name and all items of lower priority"""

    def __init__(self, name):
        self.name = name
        self.lower_priority = set()

    # Set the priority to be higher than the given item
    def set_higher(self, item):
        self.lower_priority.add(item)
        for X in item.lower_priority:
            self.lower_priority.add(X)

# Index of parent node in array
def parent(i):
    return (i - 1) >> 1

# Index of left child node in array
def left(i):
    return (i << 1) + 1

# Index of right child node in array
def right(i):
    return (i << 1) + 2


class ToDoHeap:
    """Heap data structure supporting all required operations"""

    # Construct a heap from a file, or a new heap if the filename is empty
    def __init__(self, filename):
        self.heap = []
        if not filename:
            return
        with open(filename, "r") as f:
            n = int(f.readline())
            for i in range(n):
                item = Item(f.readline().strip())
                self.heap.append(item)
            for item in self.heap:
                indices = (int(s) for s in f.readline().split())
                for i in indices:
                    item.lower_priority.add(self.heap[i])

    # Store the current heap as a file so it can be reconstructed
    def save(self, filename):
        text = str(len(self.heap))
        index = {}
        for i, item in enumerate(self.heap):
            text += "\n" + item.name
            index[item] = i
        for item in self.heap:
            text += "\n"
            for X in item.lower_priority:
                text += str(index[X]) + " "
        with open(filename, "w") as f:
            f.write(text + "\n")

    # Print the name of the item at the top of the heap
    def peek(self):
        if self.heap:
            print(self.heap[0].name)
        else:
            print(EMPTY_HEAP)

    # Add an item to the heap
    def add(self, name):
        n = len(self.heap)
        self.heap.append(Item(name))
        self._sift_up(n)
        print("Added: " + name)

    # Delete the item at the given index (in printed tree)
    def delete(self, i):
        if not self.heap:
            print(EMPTY_HEAP)
            return False
        i = self._array_index(i)
        item = self.heap[i]
        self.heap[i] = self.heap[-1]
        del self.heap[-1]
        if i == len(self.heap):
            pass        
        elif (i == 0 or self._is_higher(parent(i), i)):
            self._sift_down(i)
        else:
            self._sift_up(i)
        self._cleanup(item)
        print("Deleted: " + item.name)
        return True

    # Reset the priority of the item at the given index
    def reorder(self, i):
        i = self._array_index(i)
        item = self.heap[i]
        item.lower_priority = set()
        self._cleanup(item)
        if (i == 0):
            self._sift_down(0)
        else:
            p = parent(i)
            if self._is_higher(p, i):
                self._order_ancestors(p, item)
                self._sift_down(i)
            else:
                self._sift_up(i)
        print("Reset priority: " + item.name)

    # Rename the item at given index
    def rename(self, i, name):
        i = self._array_index(i)
        old_name = self.heap[i].name
        self.heap[i].name = name
        print("Renamed: " + old_name)
        return old_name != name

    # Print a nicely formatted binary tree
    def display(self):
        if not self.heap:
            print(EMPTY_HEAP)
            return
        max_digits = int(log10(len(self.heap))) + 1
        print("\n{:<{}}\u2553".format(0, max_digits) + self.heap[0].name)
        line = 1
        if len(self.heap) > 1:
            line = self._display(1, line, "", max_digits)
        if len(self.heap) > 2:
            self._display(2, line, "", max_digits)

    # Recursive helper function for display, returns next line number
    def _display(self, i, line, prefix, max_digits):
        print("{:<{}}".format(line, max_digits) + prefix, end="")
        line += 1
        isLastChild = ((i & 1) == 0) or (i == len(self.heap) - 1)
        if isLastChild:
            print("\u255a", end="")
            prefix += " "
        else:
            print("\u2560", end="")
            prefix += "\u2551"
        if self._is_leaf(i):
            print("\u2550" + self.heap[i].name)
        else:
            print("\u2566" + self.heap[i].name)
            line = self._display(left(i), line, prefix, max_digits)
            if self._has_two_children(i):
                line = self._display(right(i), line, prefix, max_digits)
        return line

    # Is this a valid index in the array?
    def is_valid_index(self, i):
        if (i < len(self.heap) and i >= 0):
            return True
        print("Invalid index.")
        return False

    # Sift up from the given index
    def _sift_up(self, i):
        if (i == 0):
            return
        p = parent(i)
        if self._is_higher(i, p):
            self._swap(i, p)
            self._sift_up(p)
        else:
            item = self.heap[i]
            self._order_ancestors(p, item)

    # Set the priority of all ancestors of index p to be higher than item
    def _order_ancestors(self, p, item):
        while (p != 0):
            p = parent(p)
            self.heap[p].set_higher(item)

    # Sift down from the given index
    def _sift_down(self, i):
        if self._is_leaf(i):
            return
        L = left(i)
        if self._has_two_children(i):
            R = right(i)
            if self._is_higher(L, i):
                if self._is_higher(R, L):
                    self._swap(R, i)
                    self._sift_down(R)
                else:
                    self._swap(L, i)
                    self._sift_down(L)
            elif self._is_higher(R, i):
                self._swap(R, i)
                self._sift_down(R)
        elif self._is_higher(L, i):
            self._swap(L, i)
            self._sift_down(L)

    # Is item at index i of higher priority than item at index j?  If the two
    # are not comparable, their relative priority is determined by the user.
    def _is_higher(self, i, j):
        A = self.heap[i]
        B = self.heap[j]
        if B in A.lower_priority:
            return True
        if A in B.lower_priority:
            return False
        print("1. " + A.name)
        print("2. " + B.name)
        while True:
            s = input("Higher priority: ")
            if not s:
                continue
            c = s[0]
            if c == "1":
                A.set_higher(B)
                return True
            elif c == "2":
                B.set_higher(A)
                return False

    # Remove item from all other items' lower priority sets
    def _cleanup(self, item, i=0):
        if i >= len(self.heap):
            return
        X = self.heap[i]
        if not (item in X.lower_priority):
            return
        X.lower_priority.remove(item)
        self._cleanup(item, left(i))
        self._cleanup(item, right(i))

    # Convert a node's index in the printed tree (preorder index) to its index
    # in the array (level order index)
    def _array_index(self, p):
        stack = []
        count = 0
        i = 0
        while count < p:
            if self._has_two_children(i):
                stack.append(right(i))
                stack.append(left(i))
            elif not self._is_leaf(i):
                stack.append(left(i))
            count += 1
            i = stack.pop()
        return i

    # Swap the positions of two items in the heap
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Is the node a leaf?
    def _is_leaf(self, i):
        return left(i) >= len(self.heap)

    # Does the node have two children?
    def _has_two_children(self, i):
        return right(i) < len(self.heap)

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

# Get the first command line argument if it is a valid file that exists
def get_arg():
    if len(argv) > 1:
        filename = argv[1]
        if not is_valid_filename(filename):
            print("Invalid filename.")
        elif not os.path.isfile(filename):
            print("File {} not found.".format(filename))
        else:
            return filename
    return ""

# Get a non-empty valid filename
def get_filename():
    while True:
        filename = input("Enter filename: ")
        if is_valid_filename(filename):
            return filename + ".heap"
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
        if command in ("peek", ""):
            heap.peek()
        elif command in ("list", "ls"):
            heap.display()
        elif command == "add":
            name = get_name(string)
            heap.add(name)
            changed = True
        elif command in ("delete", "del"):
            if string:
                i, _ = get_int(string)
                if heap.is_valid_index(i):
                    if heap.delete(i):
                        changed = True
            elif heap.delete(0):
                changed = True
        elif command in ("reorder", "ro"):
            i, _ = get_int(string)
            if heap.is_valid_index(i):
                heap.reorder(i)
                changed = True
        elif command in ("rename", "rn"):
            i, string = get_int(string)
            if heap.is_valid_index(i):
                name = get_name(string)
                if heap.rename(i, name):
                    changed = True
        elif command in ("quit", "q"):
            if changed and save_query():
                if not filename:
                    filename = get_filename()
                heap.save(filename)
            break
        elif command == "help":
            print(HELP)
        else:
            print(UNRECOGNIZED)

