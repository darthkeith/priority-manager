"""Module for the comparison heap's text-based user interface window.

Functions
---------
init(window: curses.window, get_lines: StrIterFunc)
    Initialize the window.
get_key_cmd(msg: str, idx: int) -> str:
    Return key from user input while displaying the command guide.
get_key_cursor(prompt: str, highlight: int = -1) -> str
    Return key from user input while showing a prompt with a cursor.
get_key(prompt: str = '', pre_msg: str = '', msg: str = '') -> str
    Return key from user input.
"""

import curses
from typing import Callable, Iterator

from data import CMD_GUIDE, ROW, ESC_DELAY
from colors import COLOR, init_colors

# Type Aliases
VoidFunc = Callable[[], None]
StrIterFunc = Callable[[], Iterator[str]]

# Global Variables
_window: curses.window = None
_get_lines: StrIterFunc = None


def init(window: curses.window, get_lines: StrIterFunc):
    """Initialize the window.

    Must be called before the other functions in the module are used.
    """
    global _window
    global _get_lines
    _window = window
    _get_lines = get_lines
    init_colors()
    _window.bkgd(COLOR['TEXT'])
    curses.set_escdelay(ESC_DELAY)


def _n_rows() -> int:
    # Return the number of visible rows in the window.
    return _window.getmaxyx()[0]


def _n_cols() -> int:
    # Return the number of visible columns in the window.
    return _window.getmaxyx()[1]


def _print_row(row: int, msg: str, color: int, highlight : bool = False):
    # Print a string on a given row in a color with optional highlight.
    if row >= _n_rows():
        return
    attr = curses.A_REVERSE if highlight else curses.A_NORMAL
    line = curses.newwin(1, max(_n_cols(), len(msg) + 1), row, 0)
    line.addstr(msg)
    line.chgat(0, 0, color | attr)
    line.overwrite(_window)


def _print_cmd_guide():
    # Print the command guide.
    row, color = ROW['PROMPT'], COLOR['PROMPT']
    _print_row(row, CMD_GUIDE['COMMANDS'], color)
    for col in CMD_GUIDE['UNDERLINE_COLS']:
        if col >= _n_cols():
            return
        _window.chgat(row, col, 1, color | curses.A_UNDERLINE)


def _print_prompt(prompt: str):
    # Print a prompt message on the prompt line.
    _print_row(ROW['PROMPT'], prompt, COLOR['PROMPT'])


def _print_prompt_cursor(prompt: str):
    # Print a prompt message on the prompt line, showing the cursor.
    _print_prompt(prompt)
    if len(prompt) < _n_cols():
        curses.curs_set(2)
        _window.move(ROW['PROMPT'], len(prompt))
    else:
        curses.curs_set(0)


def _print_msg(msg: str):
    # Print a message on the main message line.
    _print_row(ROW['MSG'], msg, COLOR['TEXT'])


def _print_msgs(pre_msg: str, msg: str):
    # Print messages on the main message line and the preceding line.
    _print_row(ROW['PRE_MSG'], pre_msg, COLOR['TEXT'])
    _print_msg(msg)


def _display_heap(highlight: int = -1):
    # Display the heap, optionally highlight a row (-1 for no highlight)
    for i, line in enumerate(_get_lines()):
        row = ROW['HEAP'] + i
        if row >= _n_rows():
            return
        _print_row(row, line, COLOR['TEXT'], i == highlight)


def _do_get_key(print_prompt: VoidFunc,
                print_msg: VoidFunc,
                highlight: int = -1) -> str:
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
            return chr(k)


def get_key_cmd(msg: str, idx: int) -> str:
    """Return key from user input while displaying the command guide.

    Display a message and highlight a row (-1 for no highlight).
    """
    print_msg = lambda: _print_msg(msg)
    return _do_get_key(_print_cmd_guide, print_msg, idx)


def get_key_cursor(prompt: str, highlight: int = -1) -> str:
    """Return key from user input while showing a prompt with a cursor.

    Optionally highlight a row (-1 for no highlight).
    """
    print_prompt = lambda: _print_prompt_cursor(prompt)
    print_msg = lambda: None
    return _do_get_key(print_prompt, print_msg, highlight)


def get_key(prompt: str = '', pre_msg: str = '', msg: str = '') -> str:
    """Return key from user input.

    Optionally display a prompt and/or messages.
    """
    print_prompt = lambda: _print_prompt(prompt)
    print_msg = lambda: _print_msgs(pre_msg, msg)
    return _do_get_key(print_prompt, print_msg)

