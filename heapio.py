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
from data import PROMPT, MESSAGE, KEY


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
        return MESSAGE['OPENED'] + filename
    else:
        heap.init(_is_higher)
        return MESSAGE['EMPTY_HEAP']


def _is_higher(item1: str, item2: str) -> bool:
    # Return True if item 1 is of higer priority than item 2.
    line1 = MESSAGE['LABEL_1'] + item1
    line2 = MESSAGE['LABEL_2'] + item2
    while True:
        key = window.get_key(PROMPT['SELECT'], line1, line2)
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
        elif key == KEY['BACKSPACE']:
            curr_str = curr_str[:-1]
        elif key in KEY['ENTER_KEYS']:
            break
        elif key == KEY['ESCAPE']:
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
        elif key == KEY['BACKSPACE']:
            curr_str = curr_str[:-1]
        elif key in KEY['ENTER_KEYS']:
            if not curr_str:
                curr_str = '-1'
            break
        elif key == KEY['ESCAPE']:
            curr_str = '-1'
            break
    return int(curr_str)


def insert() -> tuple[bool, str, int]:
    """Insert an item into the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    name = _input_str(PROMPT['INSERT'])
    if not name:
        return False, MESSAGE['CANCELED'], -1
    idx = heap.insert(name)
    return True, MESSAGE['INSERTED'] + name, idx


def delete() -> tuple[bool, str]:
    """Delete an item from the heap.

    Return tuple: (completion indicator, result message).
    """
    if heap.is_empty():
        return False, MESSAGE['EMPTY_HEAP']
    idx = _input_idx(PROMPT['DELETE'])
    if idx == -1:
        return False, MESSAGE['CANCELED']
    name = heap.delete(idx)
    return True, MESSAGE['DELETED'] + name


def move() -> tuple[bool, str, int]:
    """Delete then reinsert an item into the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    if heap.is_empty():
        return False, MESSAGE['EMPTY_HEAP'], -1
    idx = _input_idx(PROMPT['MOVE'])
    if idx == -1:
        return False, MESSAGE['CANCELED'], -1
    name, new_idx = heap.move(idx)
    return True, MESSAGE['MOVED'] + name, new_idx


def rename() -> tuple[bool, str, int]:
    """Rename an item in the heap.

    Return tuple: (completion indicator, result message, item index).
    """
    if heap.is_empty():
        return False, MESSAGE['EMPTY_HEAP'], -1
    idx = _input_idx(PROMPT['RENAME_INDEX'])
    if idx == -1:
        return False, MESSAGE['CANCELED'], -1
    name = _input_str(PROMPT['RENAME_NAME'])
    if not name:
        return False, MESSAGE['CANCELED'], -1
    heap.rename(idx, name)
    return True, MESSAGE['RENAMED'] + name, idx


def _save(filename: str) -> tuple[bool, str]:
    # Attempt to save the heap as a text file.
    # Return tuple: (completion indicator, result message).
    def write(fname: str):
        with open(fname, 'w') as f:
            for line in heap.to_preorder():
                f.write(line + '\n')
    if filename:
        write(filename)
        return True, MESSAGE['SAVED'] + filename
    filename = _input_str(PROMPT['FILENAME'])
    if not filename:
        return False, MESSAGE['CANCELED']
    if isfile(filename):
        return False, MESSAGE['FILE_EXISTS'] + filename
    try:
        write(filename)
        return True, MESSAGE['SAVED'] + filename
    except FileNotFoundError:
        return False, MESSAGE['INVALID_PATH'] + filename


def query_save(filename: str) -> tuple[bool, str]:
    """Query if the user wants to save, and save to file if so.

    Return tuple: (completion indicator, result message)
    """
    while True:
        key = window.get_key(PROMPT['SAVE'])
        if key == 'y':
            saved, message = _save(filename)
            if not saved:
                return False, message
            window.get_key(msg=message)
            return True, ''
        elif key == 'n':
            window.get_key(msg=MESSAGE['NOT_SAVED'])
            return True, ''
        elif key == KEY['ESCAPE']:
            return False, MESSAGE['CANCELED']


get_cmd = window.get_key_cmd

