"""Module for functions used by the main script.

Functions
---------
init(curses_window: curses.window, filename: str) -> str
    Initialize the module.
insert() -> tuple[bool, str, int]:
    Insert an item into the heap.
delete() -> tuple[bool, str]
    Delete an item from the heap.
move() -> tuple[bool, str, int]:
    Delete then reinsert an item into the heap.
rename() -> tuple[bool, str, int]
    Rename an item in the heap.
query_save(filename: str) -> tuple[bool, str]
    Query if the user wants to save, and save to file if so.
get_cmd(msg: str, idx: int) -> str
    Return key from user input while displaying the command guide.
"""

from os.path import isfile

import heap
import window
import data as d


def init(curses_window: 'curses.window', filename: str) -> str:
    """Initialize the module.
    
    Build heap from saved file, or build empty heap if `filename` is
    empty, and return result message.
    """
    window.init(curses_window, heap.display)
    if filename:
        with open(filename, 'r') as f:
            preorder = (s[:-1] for s in f)
            heap.init(_is_higher, preorder)
        return d.MSG_OPENED + filename
    else:
        heap.init(_is_higher)
        return d.MSG_EMPTY_HEAP


def _is_higher(item1: str, item2: str) -> bool:
    # Return True if item 1 is of higer priority than item 2.
    line1 = d.LABEL1 + item1
    line2 = d.LABEL2 + item2
    while True:
        key = window.get_key(d.PROMPT_SELECT, line1, line2)
        if key == '1':
            return True
        if key == '2':
            return False


def _input_str(prompt: str) -> str:
    # Get string from user input.
    def is_printable(c: str) -> bool:
        return ' ' <= c <= '~'
    curr_str = ''
    while True:
        key = window.get_key_cursor(prompt + curr_str)
        if is_printable(key):
            curr_str += key
        elif key == d.KEY_BACKSPACE:
            curr_str = curr_str[:-1]
        elif key in d.KEYS_ENTER:
            break
        elif key == d.KEY_ESC:
            curr_str = ''
            break
    return curr_str.strip()


def _input_idx(prompt: str) -> int:
    # Get valid index from user input.
    curr_str = '0'
    while True:
        idx = int(curr_str) if curr_str else -1
        key = window.get_key_cursor(prompt + curr_str, idx)
        if key.isdigit():
            idx = int(curr_str + key) 
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


def insert() -> tuple[bool, str, int]:
    """Insert an item into the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    name = _input_str(d.PROMPT_INSERT)
    if not name:
        return False, d.MSG_CANCELED, -1
    idx = heap.insert(name)
    return True, d.MSG_INSERTED + name, idx


def delete() -> tuple[bool, str]:
    """Delete an item from the heap.

    Return tuple: (completion indicator, result message).
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP
    idx = _input_idx(d.PROMPT_DELETE)
    if idx == -1:
        return False, d.MSG_CANCELED
    name = heap.delete(idx)
    return True, d.MSG_DELETED + name


def move() -> tuple[bool, str, int]:
    """Delete then reinsert an item into the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP, -1
    idx = _input_idx(d.PROMPT_MOVE)
    if idx == -1:
        return False, d.MSG_CANCELED, -1
    name, new_idx = heap.move(idx)
    return True, d.MSG_MOVED + name, new_idx


def rename() -> tuple[bool, str, int]:
    """Rename an item in the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    if heap.is_empty():
        return False, d.MSG_EMPTY_HEAP, -1
    idx = _input_idx(d.PROMPT_RENAME_INDEX)
    if idx == -1:
        return False, d.MSG_CANCELED, -1
    name = _input_str(d.PROMPT_RENAME_NAME)
    if not name:
        return False, d.MSG_CANCELED, -1
    heap.rename(idx, name)
    return True, d.MSG_RENAMED + name, idx


def _save(filename: str) -> tuple[bool, str]:
    # Attempt to save the heap as a text file.
    # Return tuple: (completion indicator, result message).
    def write(fname: str):
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


def query_save(filename: str) -> tuple[bool, str]:
    """Query if the user wants to save, and save to file if so.

    Return tuple: (completion indicator, result message)
    """
    while True:
        key = window.get_key(d.PROMPT_SAVE)
        if key == 'y':
            saved, message = _save(filename)
            if not saved:
                return False, message
            window.get_key(msg=message)
            return True, ''
        elif key == 'n':
            window.get_key(msg=d.MSG_NOT_SAVED)
            return True, ''
        elif key == d.KEY_ESC:
            return False, d.MSG_CANCELED


get_cmd = window.get_key_cmd

