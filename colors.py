"""Module to initialize and define color pairs.

Functions
---------
init_colors()
    Initialize colors.

Colors
------
COLOR : dict[str, int]
    Dictionary storing the following color pair attributes:

    'PROMPT'
        For prompt messages.
    'TEXT'
        For all other text.
"""

import curses

from data import NO_COLORS_ERROR

COLOR = {
    'PROMPT': 0,
    'TEXT': 0
}


def _make_counter(i):
    while True:
        yield i
        i += 1


_color_counter = _make_counter(1)
_pair_counter = _make_counter(1)


def _make_pair(foreground, background):
    i = next(_pair_counter)
    curses.init_pair(i, foreground, background)
    return curses.color_pair(i)


_PROMPT = next(_color_counter)
_PROMPT_BG = next(_color_counter)
_TEXT = next(_color_counter)
_TEXT_BG = next(_color_counter)


def init_colors():
    """Initialize colors."""
    if not curses.has_colors():
        raise RuntimeError(NO_COLORS_ERROR)
    curses.start_color()
    if not curses.can_change_color():
        curses.use_default_colors()
        return
    curses.init_color(_PROMPT, 961, 376, 220)      # F56038
    curses.init_color(_PROMPT_BG, 39, 184, 208)    # 0A2F35
    curses.init_color(_TEXT, 969, 639, 145)        # F7A325
    curses.init_color(_TEXT_BG, 71, 286, 184)      # 12492F
    COLOR['PROMPT'] = _make_pair(_PROMPT, _PROMPT_BG)
    COLOR['TEXT'] = _make_pair(_TEXT, _TEXT_BG)

