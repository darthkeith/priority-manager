# Priority Manager

Prioritize items by making pairwise comparisons via a text-based interface.
Items are stored in a heap to reduce the number of comparisons needed to
determine the highest priority item.

## Usage

```shell
./main.py [filename]
```

* `filename` (optional) - A previously saved file used to load a heap.  If no
  filename is provided, the program will start with an empty heap.

## Commands

* `i` - Insert an item into the heap.

* `d` - Delete an item from the heap.

* `m` - Move an item by deleting it and reinserting it.

* `r` - Rename an item.

* `q` - Quit after optionally saving the heap.

* `Esc` - Cancel a command.

