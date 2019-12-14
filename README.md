# To-do Heap
This is a command line program that stores items in a binary heap with priority chosen by the user such that the user makes as few comparisons as possible.

## Available Commands
`peek` or `<Enter>` - Show the item of highest priority

`list` or `ls` - Display all items

`add [name]` - Add item with given name

`delete` or `del` `[index]` - Delete the item at index (0 by default)

`reorder` or `ro` `[index]` - Reorder the item at index 

`rename` or `rn` `[index]` `[name]` - Rename the item at index

`quit` or `q` - Save and quit the program

`help` - List available commands

## Saving and Loading
A heap can be saved when quitting.  If saving a new heap, a file will be created with the ".heap" extension.

To open a saved heap, use the filename as a command line argument:

`python ToDoHeap.py filename.heap`
