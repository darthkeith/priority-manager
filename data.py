"""Module for constants."""

from typing import List
import curses

NO_COLORS_ERROR = "Terminal does not support colors."

PROMPT = {
    'SELECT': "Select higher priority.",
    'INSERT': "Insert: ",
    'DELETE': "Delete index: ",
    'MOVE': "Move index: ",
    'RENAME_INDEX': "Rename index: ",
    'RENAME_NAME': "New name: ",
    'FILENAME': "Enter filename: ",
    'SAVE': "Save? (y/n)"
}

MESSAGE = {
    'OPENED': "Opened: ",
    'LABEL_1': "(1) ",
    'LABEL_2': "(2) ",
    'EMPTY_HEAP': "Heap is empty.",
    'CANCELED': "Canceled.",
    'INSERTED': "Inserted: ",
    'DELETED': "Deleted: " ,
    'MOVED': "Moved: ",
    'RENAMED': "Renamed: ",
    'SAVED': "Saved: ",
    'FILE_EXISTS': "File already exists: ",
    'INVALID_PATH': "Invalid path: ",
    'NOT_SAVED': "Not saved."
}

KEY = {
    'ESCAPE': chr(27),
    'BACKSPACE': chr(curses.KEY_BACKSPACE),
    'ENTER_KEYS': (chr(curses.KEY_ENTER), '\n', '\r')
}

_SPACING = ' ' * 4
_COMMAND_LIST = ["insert", "delete", "move", "rename", "quit"]


def get_underline_cols() -> List[int]:
    # Return list of indices of first letters of commands to underline.
    i = len(_SPACING)
    underline_cols = []
    for cmd in _COMMAND_LIST:
        underline_cols.append(i)
        i += len(cmd) + len(_SPACING)
    return underline_cols


CMD_GUIDE = {
    'COMMANDS': _SPACING + _SPACING.join(_COMMAND_LIST),
    'UNDERLINE_COLS': get_underline_cols()
}

ROW = {
    'PROMPT': 0,
    'PRE_MSG': 1,
    'MSG': 2,
    'HEAP': 4
}

ESC_DELAY = 25    # Delay after pressing escape key, in milliseconds

