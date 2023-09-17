"""Module to initialize and define color pairs.

Functions
---------
init_colors()
    Initialize color pairs.

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
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from typing import Iterator

from data import DEFAULT_CONFIG_FILE, NO_COLORS_ERROR

COLOR = {
    'PROMPT': 0,
    'TEXT': 0
}


def _make_counter(i: int) -> Iterator[int]:
    while True:
        yield i
        i += 1


_color_counter = _make_counter(1)
_pair_counter = _make_counter(1)

_color_IDs = {
    'prompt':    next(_color_counter),
    'prompt_bg': next(_color_counter),
    'text':      next(_color_counter),
    'text_bg':   next(_color_counter)
}


def _make_pair(foreground: int, background: int) -> int:
    # Return color pair attribute given foreground/background color IDs.
    i = next(_pair_counter)
    curses.init_pair(i, foreground, background)
    return curses.color_pair(i)


def _hex_to_1000(hex_color: str) -> tuple[int, int, int]:
    # Convert 24-bit color hex string to RGB values in range [0, 1000].
    def do_convert(component: str) -> int:
        return round(int(component, 16) * 1000 / 255)
    return tuple(do_convert(hex_color[i:i+2]) for i in (0, 2, 4))


def _parse_config():
    # Parse config file to initialize individual colors.
    with open(DEFAULT_CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)
    color_scheme = config['color_schemes'][config['color_scheme']]
    color_hex_codes = config['colors']
    for feature in _color_IDs.keys():
        color_name = color_scheme[feature]
        color_hex = color_hex_codes[color_name]
        r, g, b = _hex_to_1000(color_hex)
        curses.init_color(_color_IDs[feature], r, g, b)


def init_colors():
    """Initialize color pairs."""
    if not curses.has_colors():
        raise RuntimeError(NO_COLORS_ERROR)
    curses.start_color()
    if not curses.can_change_color():
        curses.use_default_colors()
        return
    _parse_config()
    COLOR['PROMPT'] = _make_pair(_color_IDs['prompt'], _color_IDs['prompt_bg'])
    COLOR['TEXT'] = _make_pair(_color_IDs['text'], _color_IDs['text_bg'])

