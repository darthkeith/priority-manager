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
LENGTH_COMMAND_GUIDE = sum(len(c) for c in COMMANDS) + 4*len(COMMANDS) + 1
LABEL1 = "(1) "
LABEL2 = "(2) "
KEYS_ENTER = (curses.KEY_ENTER, 10, 13)
KEY_ESC = 27

ROW_PROMPT = 0
ROW_MSG = 2
ROW_TREE = 4

def is_ASCII_key(key):
    return key >= 32 and key <= 126


class ComparisonHeapTUI:
    """Text-based user interface for Comparison Heap"""
    def __init__(self):
        environ.setdefault('ESCDELAY','25') # prevent delay after pressing Esc
        curses.wrapper(self.main)

    def main(self, window):
        self.window = window
        curses.curs_set(False)
        filename = self.parse_filename()
        self.heap = ComparisonHeap(filename, self.is_higher)
        changed = False
        while True:
            self.print_command_guide()
            self.display_tree()
            cmd = window.getkey()
            self.clear_row(ROW_MSG)
            if cmd == 'a':
                if self.add():
                    changed = True
            elif cmd == 'd':
                if self.delete():
                    changed = True
            elif cmd == 'm':
                if self.move():
                    changed = True
            elif cmd == 'r':
                if self.rename():
                    changed = True
            elif cmd == 'q':
                if changed and not self.save_query(filename):
                    continue
                break

    def nrows(self):
        return self.window.getmaxyx()[0]

    def ncols(self):
        return self.window.getmaxyx()[1]

    def clear_row(self, row):
        if row >= self.nrows():
            return
        self.window.move(row, 0)
        self.window.clrtoeol()

    def print_row(self, row, msg):
        if row >= self.nrows():
            return
        self.window.move(row, 0)
        self.window.clrtoeol()
        line = curses.newwin(1, len(msg) + 1, row, 0)
        line.addstr(msg)
        line.overwrite(self.window)
    
    def print_row_cursor(self, row, msg):
        self.print_row(row, msg)
        if len(msg) < self.ncols():
            curses.curs_set(True)
            self.window.move(row, len(msg))
        else:
            curses.curs_set(False)

    def print_command_guide(self):
        self.clear_row(ROW_PROMPT)
        line = curses.newwin(1, LENGTH_COMMAND_GUIDE, 0, 0)
        for cmd in COMMANDS:
            line.addstr("    ")
            line.addstr(cmd[0], curses.A_UNDERLINE)
            line.addstr(cmd[1:])
        line.overwrite(self.window)
    
    def input_str(self, prompt):
        # Get string of basic ASCII characters from user.
        input_str = ''
        while True:
            self.print_row_cursor(ROW_PROMPT, prompt + input_str)
            key = self.window.getch()
            if is_ASCII_key(key):
                input_str += chr(key)
            elif key == curses.KEY_BACKSPACE:
                input_str = input_str[:-1]
            elif key in KEYS_ENTER:
                break
            elif key == KEY_ESC:
                input_str = ''
                break
            else:
                self.display_tree()
        input_str = input_str.strip()
        if not input_str:
            self.print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return input_str

    def input_idx(self, prompt):
        # Get integer from user.
        input_str = '0'
        while True:
            self.print_row_cursor(ROW_PROMPT, prompt + input_str)
            key = self.window.getch()
            char = chr(key)
            if char.isdigit():
                idx = int(input_str + char) 
                if self.heap.is_valid_idx(idx):
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
            else:
                self.display_tree()
        idx = int(input_str)
        if idx == -1:
            self.print_row(ROW_MSG, MSG_CANCELED)
        curses.curs_set(False)
        return idx
 
    def add(self):
        name = self.input_str(PROMPT_ADD)
        if not name:
            return False
        self.heap.add(name)
        self.print_row(ROW_MSG, MSG_ADDED + name)
        return True

    def delete(self):
        if self.heap.is_empty():
            self.print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = self.input_idx(PROMPT_DELETE)
        if idx == -1:
            return False
        name = self.heap.delete(idx)
        self.print_row(ROW_MSG, MSG_DELETED + name)
        return True

    def move(self):
        if self.heap.is_empty():
            self.print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = self.input_idx(PROMPT_MOVE)
        if idx == -1:
            return False
        name = self.heap.move(idx)
        self.print_row(ROW_MSG, MSG_MOVED + name)
        return True

    def rename(self):
        if self.heap.is_empty():
            self.print_row(ROW_MSG, MSG_EMPTY_HEAP)
            return False
        idx = self.input_idx(PROMPT_RENAME_INDEX)
        if idx == -1:
            return False
        name = self.input_str(PROMPT_RENAME_NAME)
        if not name:
            return False
        self.heap.rename(idx, name)
        self.print_row(ROW_MSG, MSG_RENAMED + name)
        return True

    def save(self, filename):
        if filename:
            self.heap.save(filename)
            return True
        while True:
            filename = self.input_str(PROMPT_FILENAME)
            if not filename:
                return False
            if isfile(filename):
                self.print_row(ROW_MSG, MSG_FILE_EXISTS)
                continue
            try:
                self.heap.save(filename)
                return True
            except FileNotFoundError:
                self.print_row(ROW_MSG, MSG_INVALID_PATH) 

    def save_query(self, filename):
        while True:
            self.print_row(ROW_PROMPT, PROMPT_SAVE)
            key = self.window.getch()
            if key == ord('y'):
                if not self.save(filename):
                    return False
                self.clear_row(ROW_PROMPT)
                self.print_row(ROW_MSG, MSG_SAVED)
                self.window.getch()
                return True
            elif key == ord('n'):
                self.clear_row(ROW_PROMPT)
                self.print_row(ROW_MSG, MSG_NOT_SAVED)
                self.window.getch()
                return True
            elif key == KEY_ESC:
                self.print_row(ROW_MSG, MSG_CANCELED)
                return False
            else:
                self.display_tree()

    def is_higher(self, item_1, item_2):
        # Is Item A of higher priority than item B?
        self.print_row(ROW_PROMPT, PROMPT_SELECT)
        self.print_row(ROW_MSG - 1, LABEL1 + item_1)
        self.print_row(ROW_MSG, LABEL2 + item_2)
        while True:
            char = self.window.getkey()
            if char == '1':
                answer = True
                break
            if char == '2':
                answer = False
                break
        self.clear_row(ROW_PROMPT)
        self.clear_row(ROW_MSG - 1)
        self.clear_row(ROW_MSG)
        return answer

    def parse_filename(self):
        # Return first command line argument if it's an existing file.
        if len(argv) > 1:
            filename = argv[1]
            if isfile(filename):
                return filename
            else:
                self.print_row(ROW_MSG, MSG_FILE_NOT_FOUND.format(filename))
        return ''

    def display_tree(self):
        # Display the heap as a tree.
        if ROW_TREE >= self.nrows():
            return
        self.window.move(ROW_TREE, 0)
        self.window.clrtobot()
        row = ROW_TREE
        for line in self.heap.display_tree():
            self.print_row(row, ''.join(line))
            row += 1

if __name__ == "__main__":
    ComparisonHeapTUI()

