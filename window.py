"""Module for the comparison heap's text-based user interface window.

Functions
---------
init(window: curses.window, get_lines: StrIterFunc)
    Initialize the window.
get_key_cmd(msg: str) -> int
    Return key from user input while displaying the command guide.
get_key_cursor(prompt: str, highlight: int = -1) -> int
    Return key from user input while showing a prompt with a cursor.
get_key(prompt: str = '', pre_msg: str = '', msg: str = '') -> int
    Return key from user input.
"""

import curses
from typing import Callable, Iterator

import data as d

# Type Aliases
VoidFunc = Callable[[], None]
StrIterFunc = Callable[[], Iterator[str]]

# Global Variables
_cmd_guide: curses.window = None
_window: curses.window = None
_get_lines: StrIterFunc = None


def init(window: curses.window, get_lines: StrIterFunc):
    """Initialize the window.

    Must be called before the other functions in the module are used.
    """
    global _cmd_guide
    global _window
    global _get_lines
    _cmd_guide = _build_cmd_guide()
    _window = window
    _get_lines = get_lines
    curses.set_escdelay(d.ESC_DELAY)


def _build_cmd_guide() -> curses.window:
    # Construct command guide to be overwritten on main window.
    width = sum(len(c) for c in d.COMMANDS) + len(d.SPACE)*len(d.COMMANDS) + 1
    pad = curses.newpad(1, width)
    for cmd in d.COMMANDS:
        pad.addstr(d.SPACE)
        pad.addstr(cmd[0], curses.A_UNDERLINE)
        pad.addstr(cmd[1:])
    return pad


def _print_cmd_guide():
    # Print the command guide.
    _cmd_guide.overwrite(_window)


def _n_rows() -> int:
    # Return the number of visible rows in the window.
    return _window.getmaxyx()[0]


def _n_cols() -> int:
    # Return the number of visible columns in the window.
    return _window.getmaxyx()[1]


def _print_row(row: int, msg: str, attr: int = curses.A_NORMAL):
    # Print a string on a given row with an optional style applied.
    if row >= _n_rows():
        return
    line = curses.newwin(1, len(msg) + 1, row, 0)
    line.addstr(msg, attr)
    line.overwrite(_window)


def _print_prompt(prompt: str):
    # Print a prompt message on the prompt line.
    _print_row(d.ROW_A_PROMPT, prompt)


def _print_prompt_cursor(prompt: str):
    # Print a prompt message on the prompt line, showing the cursor.
    _print_prompt(prompt)
    if len(prompt) < _n_cols():
        curses.curs_set(2)
        _window.move(d.ROW_A_PROMPT, len(prompt))
    else:
        curses.curs_set(0)


def _print_msg(msg: str):
    # Print a message on the main message line.
    _print_row(d.ROW_C_MSG, msg)


def _print_msgs(pre_msg: str, msg: str):
    # Print messages on the main message line and the preceding line.
    _print_row(d.ROW_B_MSG, pre_msg)
    _print_msg(msg)


def _display_heap(highlight: int = -1):
    # Display the heap, optionally highlight a row (-1 for no highlight)
    for i, line in enumerate(_get_lines()):
        row = d.ROW_D_HEAP + i
        if row >= _n_rows():
            return
        attr = curses.A_REVERSE if i == highlight else curses.A_NORMAL
        _print_row(row, line, attr)


def _do_get_key(print_prompt: VoidFunc,
                print_msg: VoidFunc,
                highlight: int = -1) -> int:
    # Get key from user input while displaying a prompt and messages.
    # Optionally hightlight a row (-1 for no highlight).
    curses.curs_set(0)
    while True:
        _window.erase()
        print_msg()
        _display_heap(highlight)
        print_prompt()   # Call last to correctly place cursor
        k = _window.getch()
        if k != curses.KEY_RESIZE:
            return k


def get_key_cmd(msg: str) -> int:
    """Return key from user input while displaying the command guide.

    Display the given message.
    """
    print_msg = lambda: _print_msg(msg)
    return _do_get_key(_print_cmd_guide, print_msg)


def get_key_cursor(prompt: str, highlight: int = -1) -> int:
    """Return key from user input while showing a prompt with a cursor.

    Optionally highlight a row (-1 for no highlight).
    """
    print_prompt = lambda: _print_prompt_cursor(prompt)
    print_msg = lambda: None
    return _do_get_key(print_prompt, print_msg, highlight)


def get_key(prompt: str = '', pre_msg: str = '', msg: str = '') -> int:
    """Return key from user input.

    Optionally display a prompt and/or messages.
    """
    print_prompt = lambda: _print_prompt(prompt)
    print_msg = lambda: _print_msgs(pre_msg, msg)
    return _do_get_key(print_prompt, print_msg)

