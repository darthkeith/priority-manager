"""
An interactive program that stores items in a heap with priority chosen by the
user such that the user makes as few comparisons as possible.

Commands:
[copy from help function]
"""

import os

DATA_DIR = "heap_data/"

class Item:
    """"An item in a heap that stores its name and all items of lower priority"""

    def __init__(self, name):
        self.name = name
        self.lower_priority = set()

class ToDoHeap:
    """Heap data structure supporting all required operations"""

    def __init__(self, name, new=False):
        """Create an empty heap or reconstruct one from a text file"""
        self.name = name
        self.heap = []
        if new:
            return
        path = DATA_DIR + name + ".heap"
        with open(path, "r") as f:
            n = int(f.readline())
            for i in range(n):
                item = Item(f.readline())
                self.heap.append(item)
            for item in self.heap:
                indices = (int(s) for s in f.readline.split())
                for i in indices:
                    item.lower_priority.add(self.heap[i])

    def save(self):
        """Store the current heap as a file so it can be reconstructed"""
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        path = DATA_DIR + self.name + ".heap"
        text = str(len(self.heap))
        index = {}
        for i, item in enumerate(self.heap):
            text += "\n" + item.name
            index[item] = i
        for item in self.heap:
            text += "\n"
            for x in item.lower_priority:
                text += str(index[x]) + " "
        with open(path, "w") as f:
            f.write(text + "\n")

    def peek(self):
        """Print the name of the item at the top of the heap"""
        if self.heap:
            print(self.heap[0].name)
        else:
            print("Heap is empty.")

    def add(self, name):
        """Add an item to the heap"""
        n = len(self.heap)
        self.heap.append(Item(name))
        self._sift_up(n)
        print("Added: " + name)

    def delete(self):
        """Delete the item at the top of the heap"""
        if not self.heap:
            print("Heap is empty.")
            return
        name = self.heap[0].name
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self._sift_down(0)
        print("Deleted: " + name)

    def display(self):
        """Print a nicely formatted binary tree"""
        if not self.heap:
            print("Heap is empty.")
            return
        print("\n\u2553" + self.heap[0].name)
        if len(self.heap) > 1:
            self._display(1, "")
        if len(self.heap) > 2:
            self._display(2, "")

    # Recursive helper function for display
    def _display(self, i, prefix):
        print(prefix, end="")
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
            self._display(self._left(i), prefix)
            if self._has_two_children(i):
                self._display(self._right(i), prefix)

    # Sift up from the given index
    def _sift_up(self, i):
        if (i == 0):
            return
        parent = self._parent(i)
        if self._is_higher(i, parent):
            self._swap(i, parent)
            self._sift_up(parent)

    # Sift down from the given index
    def _sift_down(self, i):
        if self._is_leaf(i):
            return
        left = self._left(i)
        if self._has_two_children(i):
            right = self._right(i)
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
        X = self._choice(A, B)
        Y = B if X == A else A
        self._set_higher(X, Y)
        return X == A

    # Set the priority of item A to be higher than that of item B
    def _set_higher(self, A, B):
        A.lower_priority.add(B)
        for X in B.lower_priority:
            A.lower_priority.add(X)

    # Swap the positions of two items in the heap
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Index of parent node in array
    def _parent(self, i):
        return (i - 1) >> 1

    # Index of left child node in array
    def _left(self, i):
        return (i << 1) + 1

    # Index of right child node in array
    def _right(self, i):
        return (i << 1) + 2

    # Is the node a leaf?
    def _is_leaf(self, i):
        return self._left(i) >= len(self.heap)

    # Does the node have two children?
    def _has_two_children(self, i):
        return self._right(i) < len(self.heap)

    # Ask the user to select the item of greater priority
    def _choice(self, A, B):
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

def get_name():
    """Ask the user to enter a name"""
    while True:
        name = input("Enter name: ")
        if name:
            return name

def help():
    """Display a list of all available commands"""
    # Commands:
    # new [name], open [name], listheaps, delete [heap], save?, quit, clean?
    # add, delete ([item]), reorder?, moveToTop?
    # peek, view
    pass

if __name__ == "__main__":
    heap = ToDoHeap(input("Enter heap name: "), new=True)
    while True:
        print()
        line = input(">>> ").split(None, 1)
        if line:
            command = line[0].lower()
            string = ""
            if len(line) > 1:
                string = line[1]
        else:
            continue
        
        if command == "peek":
            heap.peek()
        elif command == "add":
            if not string:
                string = get_name()
            heap.add(string)
        elif command == "del":
            heap.delete()
        elif command == "view":
            heap.display()
        elif command == "save":
            heap.save()
        elif command == "load":
            pass
        elif command in ("quit", "q"):
            break
        else:
            print("\nCommand not recognized.")
            print('Type "help" for list of available commands.')
