#!/usr/bin/env python3
"""Main script for comparison heap program.

To open a saved file, provide the filename as the first command line argument,
otherwise the program starts with an empty heap.
"""

from sys import argv
from os.path import isfile
import curses

import heapio as heap


def parse_filename() -> str:
    # Return first command line argument if it's an existing file.
    if len(argv) > 1:
        filename = argv[1]
        if not isfile(filename):
            raise FileNotFoundError(filename)
        return filename
    return ''


def main(window: curses.window):
    filename = parse_filename()
    message = heap.init(window, filename)
    idx = -1
    altered = False
    dispatch = {'i': heap.insert,
                'd': lambda: heap.delete() + (-1,),
                'm': heap.move,
                'r': heap.rename}
    while True:
        cmd = heap.get_cmd(message, idx)
        if cmd == 'q':
            if not altered:
                return
            done, message = heap.query_save(filename)
            if done:
                return
            idx = -1
        elif cmd in dispatch:
            change, message, idx = dispatch[cmd]()
            altered = altered or change
        else:
            message = ''
            idx = -1


curses.wrapper(main)

