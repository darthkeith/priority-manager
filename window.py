"""Module for the comparison heap's text-based user interface window.

Functions
---------
init
    Initialize the window.
get_key_cmd
    Return key from user input while displaying the command guide.
get_key_cursor
    Return key from user input while showing a prompt with a cursor.
get_key
    Return key from user input.
"""

import curses

import data as d


def init(window, get_lines):
    """Initialize the window.

    Must be called before the other functions in the module are used.

    Parameters
    ----------
    window
        Main curses window object.
    get_lines : function
        Callback function that returns a list of strings used to display
        the heap.
    """
    curses.set_escdelay(d.ESC_DELAY)
    global _window
    _window = window
    global _get_lines
    _get_lines = get_lines
    cmd_guide = _build_cmd_guide()
    global _print_cmd_guide
    _print_cmd_guide = lambda: cmd_guide.overwrite(window)  # Prints in 1st row


def _build_cmd_guide():
    # Construct command guide to be overwritten on main window.
    width = sum(len(c) for c in d.COMMANDS) + len(d.SPACE)*len(d.COMMANDS) + 1
    pad = curses.newpad(1, width)
    for cmd in d.COMMANDS:
        pad.addstr(d.SPACE)
        pad.addstr(cmd[0], curses.A_UNDERLINE)
        pad.addstr(cmd[1:])
    return pad


def _n_rows():
    # Return the number of visible rows in the window.
    return _window.getmaxyx()[0]


def _n_cols():
    # Return the number of visible columns in the window.
    return _window.getmaxyx()[1]


def _print_row(row, msg, attr=curses.A_NORMAL):
    # Print a string on a given row with an optional style applied.
    if row >= _n_rows():
        return
    line = curses.newwin(1, len(msg) + 1, row, 0)
    line.addstr(msg, attr)
    line.overwrite(_window)


def _print_prompt(prompt):
    # Print a prompt message on the prompt line.
    _print_row(d.ROW_A_PROMPT, prompt)


def _print_prompt_cursor(prompt):
    # Print a prompt message on the prompt line, showing the cursor.
    _print_prompt(prompt)
    if len(prompt) < _n_cols():
        curses.curs_set(2)
        _window.move(d.ROW_A_PROMPT, len(prompt))
    else:
        curses.curs_set(0)


def _print_msg(msg):
    # Print a message on the main message line.
    _print_row(d.ROW_C_MSG, msg)


def _print_msgs(pre_msg, msg):
    # Print messages on the main message line and the preceding line.
    _print_row(d.ROW_B_MSG, pre_msg)
    _print_msg(msg)


def _display_heap(highlight=-1):
    # Display the heap, optionally highlight a row (-1 for no highlight)
    for i, line in enumerate(_get_lines()):
        row = d.ROW_D_HEAP + i
        if row >= _n_rows():
            return
        attr = curses.A_REVERSE if i == highlight else curses.A_NORMAL
        _print_row(row, line, attr)


def _do_get_key(print_prompt, print_msg, highlight=-1):
    # Get key from user input while displaying a prompt and messages
    # with callback functions `print_prompt` and `print_msg`.
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


def get_key_cmd(msg):
    """Return key from user input while displaying the command guide.

    Also display the given message.
    """
    print_msg = lambda: _print_msg(msg)
    return _do_get_key(_print_cmd_guide, print_msg)


def get_key_cursor(prompt, highlight=-1):
    """Return key from user input while showing a prompt with a cursor.

    Optionally highlight a row (-1 for no highlight).
    """
    print_prompt = lambda: _print_prompt_cursor(prompt)
    print_msg = lambda: None
    return _do_get_key(print_prompt, print_msg, highlight)


def get_key(prompt='', pre_msg='', msg=''):
    """Return key from user input.

    Optionally display a prompt and/or messages.
    """
    print_prompt = lambda: _print_prompt(prompt)
    print_msg = lambda: _print_msgs(pre_msg, msg)
    return _do_get_key(print_prompt, print_msg)

