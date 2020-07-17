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
LABEL1 = "(1) "
LABEL2 = "(2) "
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

    def print_row(row, msg):
        if row >= nrows():
            return
        window.move(row, 0)
        window.clrtoeol()
        line = curses.newwin(1, len(msg) + 1, row, 0)
        line.addstr(msg)
        line.overwrite(window)
    
    def print_row_cursor(row, msg):
        print_row(row, msg)
        if len(msg) < ncols():
            curses.curs_set(True)
            window.move(row, len(msg))
        else:
            curses.curs_set(False)

    def print_command_guide():
        clear_row(ROW_PROMPT)
        line = curses.newwin(1, LENGTH_COMMAND_GUIDE, 0, 0)
        for cmd in COMMANDS:
            line.addstr(SPACING)
            line.addstr(cmd[0], curses.A_UNDERLINE)
            line.addstr(cmd[1:])
        line.overwrite(window)
    
    def is_ASCII_key(key):
        return key >= 32 and key <= 126

    def input_str(prompt):
        # Get string of basic ASCII characters from user.
        input_str = ''
        while True:
            print_row_cursor(ROW_PROMPT, prompt + input_str)
            key = window.getch()
            if is_ASCII_key(key):
                input_str += chr(key)
            elif key == curses.KEY_BACKSPACE:
                input_str = input_str[:-1]
            elif key in KEYS_ENTER:
                break
            elif key == KEY_ESC:
                input_str = ''
                break
            elif key == curses.KEY_RESIZE:
                display_tree()
        input_str = input_str.strip()
        if not input_str:
            print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return input_str

    def input_idx(prompt):
        # Get valid index from user.
        input_str = '0'
        while True:
            print_row_cursor(ROW_PROMPT, prompt + input_str)
            key = window.getch()
            char = chr(key)
            if char.isdigit():
                idx = int(input_str + char) 
                if heap.is_valid_idx(idx):
                    input_str = str(idx)
            elif key == curses.KEY_BACKSPACE:
                input_str = input_str[:-1]
            elif key in KEYS_ENTER:
                if not input_str:
                    input_str = '-1'
                break
            elif key == KEY_ESC:
                input_str = '-1'
                break
            elif key == curses.KEY_RESIZE:
                display_tree()
        idx = int(input_str)
        if idx == -1:
            print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return idx
 
    def add():
        name = input_str(PROMPT_ADD)
        if not name:
            return False
        heap.add(name)
        print_row(ROW_MSG, MSG_ADDED + name)
        return True

    def delete():
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_DELETE)
        if idx == -1:
            return False
        name = heap.delete(idx)
        print_row(ROW_MSG, MSG_DELETED + name)
        return True

    def move():
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_MOVE)
        if idx == -1:
            return False
        name = heap.move(idx)
        print_row(ROW_MSG, MSG_MOVED + name)
        return True

    def rename():
        if heap.is_empty():
            print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = input_idx(PROMPT_RENAME_INDEX)
        if idx == -1:
            return False
        name = input_str(PROMPT_RENAME_NAME)
        if not name:
            return False
        heap.rename(idx, name)
        print_row(ROW_MSG, MSG_RENAMED + name)
        return True

    def save(filename):
        if filename:
            heap.save(filename)
            return True
        while True:
            filename = input_str(PROMPT_FILENAME)
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

    def save_query(filename):
        while True:
            print_row(ROW_PROMPT, PROMPT_SAVE)
            key = window.getch()
            if key == ord('y'):
                if not save(filename):
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
            else:
                display_tree()

    def is_higher(item_1, item_2):
        # Is Item A of higher priority than item B?
        print_row(ROW_PROMPT, PROMPT_SELECT)
        print_row(ROW_MSG - 1, LABEL1 + item_1)
        print_row(ROW_MSG, LABEL2 + item_2)
        while True:
            char = window.getkey()
            if char == '1':
                answer = True
                break
            if char == '2':
                answer = False
                break
        clear_row(ROW_PROMPT)
        clear_row(ROW_MSG - 1)
        clear_row(ROW_MSG)
        return answer

    def parse_filename():
        # Return first command line argument if it's an existing file.
        if len(argv) > 1:
            filename = argv[1]
            if isfile(filename):
                return filename
            else:
                print_row(ROW_MSG, MSG_FILE_NOT_FOUND.format(filename))
        return ''

    def display_tree():
        # Display the heap as a tree.
        if ROW_TREE >= nrows():
            return
        window.move(ROW_TREE, 0)
        window.clrtobot()
        row = ROW_TREE
        for line in heap.display_tree():
            print_row(row, ''.join(line))
            row += 1

    curses.curs_set(False)
    filename = parse_filename()
    heap = ComparisonHeap(filename, is_higher)
    changed = False
    while True:
        print_command_guide()
        display_tree()
        cmd = window.getkey()
        clear_row(ROW_MSG)
        if cmd == 'a':
            if add():
                changed = True
        elif cmd == 'd':
            if delete():
                changed = True
        elif cmd == 'm':
            if move():
                changed = True
        elif cmd == 'r':
            if rename():
                changed = True
        elif cmd == 'q':
            if not changed:
                break
            if save_query(filename):
                break

if __name__ == "__main__":
    environ.setdefault('ESCDELAY','25')     # prevent delay after pressing Esc
    curses.wrapper(main)

