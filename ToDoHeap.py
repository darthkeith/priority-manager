"""
This is a command line program that stores items in a heap with priority chosen
by the user such that the user makes as few comparisons as possible.
"""

import os
from math import log10

DATA_FILE = "heap_data"
HELP = """
peek OR <Enter> - print the item of highest priority

add [name] - add item with given name

delete or del - delete the item of highest priority

list OR ls - display all items

quit OR q - quit the program

help - list available commands"""

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

class ToDoHeap:
    """Heap data structure supporting all required operations"""

    # Create an empty heap or reconstruct one from a file if it exists
    def __init__(self):
        self.heap = []
        if not os.path.isfile(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            n = int(f.readline())
            for i in range(n):
                item = Item(f.readline().strip())
                self.heap.append(item)
            for item in self.heap:
                indices = (int(s) for s in f.readline().split())
                for i in indices:
                    item.lower_priority.add(self.heap[i])

    # Store the current heap as a file so it can be reconstructed
    def save(self):
        text = str(len(self.heap))
        index = {}
        for i, item in enumerate(self.heap):
            text += "\n" + item.name
            index[item] = i
        for item in self.heap:
            text += "\n"
            for x in item.lower_priority:
                text += str(index[x]) + " "
        with open(DATA_FILE, "w") as f:
            f.write(text + "\n")

    # Print the name of the item at the top of the heap
    def peek(self):
        if self.heap:
            print(self.heap[0].name)
        else:
            print("Heap is empty.")

    # Add an item to the heap
    def add(self, name):
        n = len(self.heap)
        self.heap.append(Item(name))
        self._sift_up(n)
        print("Added: " + name)

    # Delete the item at the top of the heap
    def delete(self):
        if not self.heap:
            print("Heap is empty.")
            return
        name = self.heap[0].name
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self._sift_down(0)
        print("Deleted: " + name)

    # Print a nicely formatted binary tree
    def display(self):
        if not self.heap:
            print("Heap is empty.")
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
            line = self._display(get_left(i), line, prefix, max_digits)
            if self._has_two_children(i):
                line = self._display(get_right(i), line, prefix, max_digits)
        return line

    # Sift up from the given index
    def _sift_up(self, i):
        if (i == 0):
            return
        parent = get_parent(i)
        if self._is_higher(i, parent):
            self._swap(i, parent)
            self._sift_up(parent)
        else:
            self._set_ancestors(parent, self.heap[i])

    # Set the priority of all ancestors of a node to be higher than given item
    def _set_ancestors(self, i, item):
        if (i == 0):
            return
        p = get_parent(i)
        self.heap[p].set_higher(item)
        self._set_ancestors(p, item)

    # Sift down from the given index
    def _sift_down(self, i):
        if self._is_leaf(i):
            return
        left = get_left(i)
        if self._has_two_children(i):
            right = get_right(i)
            if self._is_higher(left, i):
                if self._is_higher(right, left):
                    self._swap(right, i)
                    self._sift_down(right)
                else:
                    self._swap(left, i)
                    self._sift_down(left)
            elif self._is_higher(right, i):
                self._swap(right, i)
                self._sift_down(right)
        elif self._is_higher(left, i):
            self._swap(left, i)
            self._sift_down(left)

    # Is item at index i of higher priority than item at index j?  If the two
    # are not comparable, their relative priority is determined by the user.
    def _is_higher(self, i, j):
        A = self.heap[i]
        B = self.heap[j]
        if B in A.lower_priority:
            return True
        if A in B.lower_priority:
            return False
        X = choice(A, B)
        Y = B if X == A else A
        X.set_higher(Y)
        return X == A

    # Swap the positions of two items in the heap
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Is the node a leaf?
    def _is_leaf(self, i):
        return get_left(i) >= len(self.heap)

    # Does the node have two children?
    def _has_two_children(self, i):
        return get_right(i) < len(self.heap)

# Index of parent node in array
def get_parent(i):
    return (i - 1) >> 1

# Index of left child node in array
def get_left(i):
    return (i << 1) + 1

# Index of right child node in array
def get_right(i):
    return (i << 1) + 2

# Ask the user to select the item of greater priority
def choice(A, B):
    print("1. " + A.name)
    print("2. " + B.name)
    while True:
        s = input("Select: ")
        if not s:
            continue
        c = s[0]
        if c == "1":
            X = A
        elif c == "2":
            X = B
        else:
            continue
        return X

# Parse user input for command and optional string after command
def get_line():
    line = input("\n>>> ").split(None, 1)
    if line:
        command = line[0].lower()
        string = ""
        if len(line) > 1:
            string = line[1]
        return command, string
    return "", ""

# Ask the user to enter a name
def get_name():
    while True:
        name = input("Enter name: ")
        if name:
            return name

if __name__ == "__main__":
    heap = ToDoHeap()
    heap.peek()
    while True:
        command, string = get_line()        
        if command in ("peek", ""):
            heap.peek()
        elif command == "add":
            if not string:
                string = get_name()
            heap.add(string)
        elif command in ("delete", "del"):
            heap.delete()
        elif command in ("list", "ls"):
            heap.display()
        elif command in ("quit", "q"):
            heap.save()
            break
        elif command == "help":
            print(HELP)
        else:
            print("\nCommand not recognized.")
            print('Type "help" for list of available commands.')

