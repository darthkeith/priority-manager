"""Module for functions used by the main comparison heap script.

Functions
---------
init
    Initialize the module.
insert
    Insert an item into the heap.
delete
    Delete an item from the heap.
move
    Delete then reinsert an item into the heap.
rename
    Rename an item in the heap.
query_save
    Query if the user wants to save, and save to file if so.
get_cmd
    Return a character from user input.
"""

from os.path import isfile

import heap
import window
import data as d


def init(curses_window, filename):
    """Initialize the module.
    
    If `filename` is an empty string, construct an empty heap.
    """
    window.init(curses_window, heap.display)
    def is_higher(item1, item2):
        # Return True if item 1 is of higer priority than item 2.
        line1 = d.LABEL1 + item1
        line2 = d.LABEL2 + item2
        while True:
            key = window.get_key(d.PROMPT_SELECT, line1, line2)
            if key == ord('1'):
                return True
            if key == ord('2'):
                return False
    if filename:
        with open(filename, 'r') as f:
            preorder = (s[:-1] for s in f)
            heap.init(is_higher, preorder)
    else:
        heap.init(is_higher)


def _input_str(prompt):
    # Get string from user input.
    def is_ASCII_char(n):
        return n >= 32 and n <= 126
    curr_str = ''
    while True:
        key = window.get_key_cursor(prompt + curr_str)
        if is_ASCII_char(key):
            curr_str += chr(key)
        elif key == d.KEY_BACKSPACE:
            curr_str = curr_str[:-1]
        elif key in d.KEYS_ENTER:
            break
        elif key == d.KEY_ESC:
            curr_str = ''
            break
    return curr_str.strip()


def _input_idx(prompt):
    # Get valid index from user input.
    curr_str = '0'
    while True:
        idx = int(curr_str) if curr_str else -1
        key = window.get_key_cursor(prompt + curr_str, idx)
        char = chr(key)
        if char.isdigit():
            idx = int(curr_str + char) 
            if heap.is_valid_idx(idx):
                curr_str = str(idx)
        elif key == d.KEY_BACKSPACE:
            curr_str = curr_str[:-1]
        elif key in d.KEYS_ENTER:
            if not curr_str:
                curr_str = '-1'
            break
        elif key == d.KEY_ESC:
            curr_str = '-1'
            break
    return int(curr_str)


def insert():
    """Insert an item into the heap.

    Return `True` if successful.
    """
    name = _input_str(d.PROMPT_INSERT)
    if not name:
        return False, d.MSG_CANCELED
    heap.insert(name)
    return True, d.MSG_INSERTED + name


def delete():
    """Delete an item from the heap.

    Return `True` if successful.
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP
    idx = _input_idx(d.PROMPT_DELETE)
    if idx == -1:
        return False, d.MSG_CANCELED
    name = heap.delete(idx)
    return True, d.MSG_DELETED + name


def move():
    """Delete then reinsert an item into the heap.

    Return `True` if successful.
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP
    idx = _input_idx(d.PROMPT_MOVE)
    if idx == -1:
        return False, d.MSG_CANCELED
    name = heap.move(idx)
    return True, d.MSG_MOVED + name


def rename():
    """Rename an item in the heap.

    Return `True` if successful.
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP
    idx = _input_idx(d.PROMPT_RENAME_INDEX)
    if idx == -1:
        return False, d.MSG_CANCELED
    name = _input_str(d.PROMPT_RENAME_NAME)
    if not name:
        return False, d.MSG_CANCELED
    heap.rename(idx, name)
    return True, d.MSG_RENAMED + name


def _save(filename):
    # Attempt to save the heap as a text file.
    # Return `True` if successful, and also a result message.
    def write(fname):
        with open(fname, 'w') as f:
            for line in heap.to_preorder():
                f.write(line + '\n')
    if filename:
        write(filename)
        return True, d.MSG_SAVED + filename
    filename = _input_str(d.PROMPT_FILENAME)
    if not filename:
        return False, d.MSG_CANCELED
    if isfile(filename):
        return False, d.MSG_FILE_EXISTS + filename
    try:
        write(filename)
        return True, d.MSG_SAVED + filename
    except FileNotFoundError:
        return False, d.MSG_INVALID_PATH + filename


def query_save(filename):
    """Query if the user wants to save, and save to file if so.

    Return `True` if query is completed successfully.
    """
    while True:
        key = window.get_key(d.PROMPT_SAVE)
        if key == ord('y'):
            saved, message = _save(filename)
            if not saved:
                return False, message
            window.get_key(msg=message)
            return True, ''
        elif key == ord('n'):
            window.get_key(msg=d.MSG_NOT_SAVED)
            return True, ''
        elif key == d.KEY_ESC:
            return False, d.MSG_CANCELED


def get_cmd(msg):
    """Return a character from user input.

    Display the given message while waiting for user input.
    """
    key = window.get_key_cmd(msg)
    return chr(key)

