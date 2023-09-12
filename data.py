"""Data for comparison heap program."""

import curses

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

TEXT = {
    'LABEL1': "(1) ",
    'LABEL2': "(2) ",
    'SPACING': "    ",
    'COMMANDS': ("insert", "delete", "move", "rename", "quit")
}

KEY = {
    'ESCAPE': chr(27),
    'BACKSPACE': chr(curses.KEY_BACKSPACE),
    'ENTER_KEYS': (chr(curses.KEY_ENTER), '\n', '\r')
}

ROW = {
    'PROMPT': 0,
    'PRE_MSG': 1,
    'MSG': 2,
    'HEAP': 4
}

ESC_DELAY = 25    # Delay after pressing escape key in milliseconds

