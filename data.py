"""Data for comparison heap program."""

from curses import KEY_ENTER, KEY_BACKSPACE

PROMPT_INSERT = "Insert: "
PROMPT_DELETE = "Delete index: "
PROMPT_MOVE = "Move index: "
PROMPT_RENAME_INDEX = "Rename index: "
PROMPT_RENAME_NAME = "New name: "
PROMPT_SAVE = "Save? (y/n)"
PROMPT_FILENAME = "Enter filename: "
PROMPT_SELECT = "Select higher priority."

MSG_EMPTY_HEAP = "Heap is empty."
MSG_INSERTED = "Inserted: "
MSG_DELETED = "Deleted: " 
MSG_MOVED = "Moved: "
MSG_RENAMED = "Renamed: "
MSG_CANCELED = "Canceled."
MSG_FILE_EXISTS = "File already exists: "
MSG_INVALID_PATH = "Invalid path: "
MSG_NOT_SAVED = "Not saved."
MSG_SAVED = "Saved: "
MSG_OPENED = "Opened: "

LABEL1 = "(1) "
LABEL2 = "(2) "
COMMANDS = ("insert", "delete", "move", "rename", "quit")
SPACE = "    "

KEY_ESC = 27
KEYS_ENTER = (KEY_ENTER, 10, 13)    # Possible codes for enter key

ROW_A_PROMPT = 0    # Prompt row
ROW_B_MSG = 1       # Supplementary message row
ROW_C_MSG = 2       # Main message row
ROW_D_HEAP = 4      # First heap row

ESC_DELAY = 25    # Delay after pressing escape key in milliseconds

