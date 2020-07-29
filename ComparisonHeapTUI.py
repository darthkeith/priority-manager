#!/usr/bin/env python3

import curses
from sys import argv
from os.path import isfile
from os import environ
from ComparisonHeap import ComparisonHeap

PROMPT_ADD = "Add: "
PROMPT_DELETE = "Delete index: "
PROMPT_MOVE = "Move index: "
PROMPT_RENAME_INDEX = "Rename index: "
PROMPT_RENAME_NAME = "New name: "
PROMPT_SAVE = "Save? (y/n)"
PROMPT_FILENAME = "Enter filename: "
PROMPT_SELECT = "Select higher priority."

MSG_FILE_NOT_FOUND = "File {} not found."
MSG_EMPTY_HEAP = "Heap is empty."
MSG_ADDED = "Added: "
MSG_DELETED = "Deleted: " 
MSG_MOVED = "Moved: "
MSG_RENAMED = "Renamed: "
MSG_CANCELED = "Canceled."
MSG_INVALID_PATH = "Invalid path."
MSG_FILE_EXISTS = "File already exists."
MSG_NOT_SAVED = "Not saved."
MSG_SAVED = "Saved."

COMMANDS = ("add", "delete", "move", "rename", "quit")
SPACING = "    "
LENGTH_COMMAND_GUIDE = (sum(len(c) for c in COMMANDS) +
                        len(SPACING)*len(COMMANDS) + 1)
LABEL_A = "(1) "
LABEL_B = "(2) "
KEYS_ENTER = (curses.KEY_ENTER, 10, 13)
KEY_ESC = 27

ROW_PROMPT = 0
ROW_MSG = 2
ROW_TREE = 4

def main(window):
    def nrows():
        return window.getmaxyx()[0]

    def ncols():
        return window.getmaxyx()[1]

    def clear_row(row):
        if row >= nrows():
            return
        window.move(row, 0)
        window.clrtoeol()

    def print_command_guide():
        clear_row(ROW_PROMPT)
        line = curses.newwin(1, LENGTH_COMMAND_GUIDE, 0, 0)
        for cmd in COMMANDS:
            line.addstr(SPACING)
            line.addstr(cmd[0], curses.A_UNDERLINE)
            line.addstr(cmd[1:])
        line.overwrite(window)
    
    def print_row(row, msg, attr=curses.A_NORMAL):
        if row >= nrows():
            return
        window.move(row, 0)
        window.clrtoeol()
        line = curses.newwin(1, len(msg) + 1, row, 0)
        line.addstr(msg, attr)
        line.overwrite(window)
    
    def print_row_cursor(row, msg):
        print_row(row, msg)
        if len(msg) < ncols():
            curses.curs_set(True)
            window.move(row, len(msg))
        else:
            curses.curs_set(False)

    def display_func():
        # Return callback function that displays the heap as a tree.
        lines = heap.display_tree()
        def display(highlight=-1):
            if ROW_TREE >= nrows():
                return
            window.move(ROW_TREE, 0)
            window.clrtobot()
            for i, triple in enumerate(lines):
                row = ROW_TREE + i
                line = ''.join(triple)
                if i == highlight:
                    print_row(row, line, curses.A_REVERSE)
                else:
                    print_row(row, line)
        return display

    def is_higher_func(display):
        # Return function that tests if item A is of higher priority than item B.
        def clear():
            clear_row(ROW_PROMPT)
            clear_row(ROW_MSG - 1)
            clear_row(ROW_MSG)
        def is_higher(item_A, item_B):
            while True:
                print_row(ROW_PROMPT, PROMPT_SELECT)
                print_row(ROW_MSG - 1, LABEL_A + item_A)
                print_row(ROW_MSG, LABEL_B + item_B)
                key = window.getch()
                if key == ord('1'):
                    clear()
                    return True
                if key == ord('2'):
                    clear()
                    return False
                if key == curses.KEY_RESIZE:
                    display()
        return is_higher

    def is_ASCII_key(key):
        return key >= 32 and key <= 126

    def input_str(prompt, display):
        # Get string of basic ASCII characters from user.
        current_str = ''
        while True:
            print_row_cursor(ROW_PROMPT, prompt + current_str)
            key = window.getch()
            if is_ASCII_key(key):
                current_str += chr(key)
            elif key == curses.KEY_BACKSPACE:
                current_str = current_str[:-1]
            elif key in KEYS_ENTER:
                break
            elif key == KEY_ESC:
                current_str = ''
                break
            elif key == curses.KEY_RESIZE:
                display()
        current_str = current_str.strip()
        if not current_str:
            print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return current_str

    def input_idx(prompt, display):
        # Get valid index from user.
        current_str = '0'
        while True:
            idx = int(current_str) if current_str else -1
            display(idx)
            print_row_cursor(ROW_PROMPT, prompt + current_str)
            key = window.getch()
            char = chr(key)
            if char.isdigit():
                idx = int(current_str + char) 
                if heap.is_valid_idx(idx):
                    current_str = str(idx)
            elif key == curses.KEY_BACKSPACE:
                current_str = current_str[:-1]
            elif key in KEYS_ENTER:
                if not current_str:
                    current_str = '-1'
                break
            elif key == KEY_ESC:
                current_str = '-1'
                break
        idx = int(current_str)
        if idx == -1:
            print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return idx
 
    def add(display):
        name = input_str(PROMPT_ADD, display)
        if not name:
            return False
        heap.add(name, is_higher_func(display))
        print_row(ROW_MSG, MSG_ADDED + name)
        return True

    def delete(display):
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_DELETE, display)
        if idx == -1:
            return False
        is_higher = is_higher_func(lambda: display(idx))
        name = heap.delete(idx, is_higher)
        print_row(ROW_MSG, MSG_DELETED + name)
        return True

    def move(display):
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_MOVE, display)
        if idx == -1:
            return False
        is_higher = is_higher_func(lambda: display(idx))
        name = heap.move(idx, is_higher)
        print_row(ROW_MSG, MSG_MOVED + name)
        return True

    def rename(display):
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_RENAME_INDEX, display)
        if idx == -1:
            return False
        name = input_str(PROMPT_RENAME_NAME, lambda: display(idx))
        if not name:
            return False
        heap.rename(idx, name)
        print_row(ROW_MSG, MSG_RENAMED + name)
        return True

    def save(filename, display):
        if filename:
            heap.save(filename)
            return True
        while True:
            filename = input_str(PROMPT_FILENAME, display)
            if not filename:
                return False
            if isfile(filename):
                print_row(ROW_MSG, MSG_FILE_EXISTS)
                continue
            try:
                heap.save(filename)
                return True
            except FileNotFoundError:
                print_row(ROW_MSG, MSG_INVALID_PATH) 

    def save_query(filename, display):
        while True:
            print_row(ROW_PROMPT, PROMPT_SAVE)
            key = window.getch()
            if key == ord('y'):
                if not save(filename, display):
                    return False
                clear_row(ROW_PROMPT)
                print_row(ROW_MSG, MSG_SAVED)
                window.getch()
                return True
            elif key == ord('n'):
                clear_row(ROW_PROMPT)
                print_row(ROW_MSG, MSG_NOT_SAVED)
                window.getch()
                return True
            elif key == KEY_ESC:
                print_row(ROW_MSG, MSG_CANCELED)
                return False
            elif key == curses.KEY_RESIZE:
                display()

    def parse_filename():
        # Return first command line argument if it's an existing file.
        if len(argv) > 1:
            filename = argv[1]
            if isfile(filename):
                return filename
            else:
                print_row(ROW_MSG, MSG_FILE_NOT_FOUND.format(filename))
        return ''

    curses.curs_set(False)
    filename = parse_filename()
    heap = ComparisonHeap(filename)
    changed = False
    while True:
        print_command_guide()
        display = display_func()
        display()
        cmd = window.getkey()
        clear_row(ROW_MSG)
        if cmd == 'a':
            if add(display):
                changed = True
        elif cmd == 'd':
            if delete(display):
                changed = True
        elif cmd == 'm':
            if move(display):
                changed = True
        elif cmd == 'r':
            if rename(display):
                changed = True
        elif cmd == 'q':
            if not changed:
                return
            if save_query(filename, display):
                return

if __name__ == "__main__":
    environ.setdefault('ESCDELAY','25')     # prevent delay after pressing Esc
    curses.wrapper(main)

