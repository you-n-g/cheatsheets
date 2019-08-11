# https://stackoverflow.com/a/18937214

# Here is a typical way to implement a curses printer

import curses
import atexit


class StatusPrinter:
    def __init__(self, dummy=False):
        self.dummy = dummy
        if self.dummy:
            return
        self.stdscr = curses.initscr()
        self.cur_line = 0

    def print(self, content):
        if self.dummy:
            return
        try:
            self.stdscr.addstr(self.cur_line, 0, str(content))
            self.stdscr.clrtoeol()
        except curses.error:
            # The window size may be smaller than you want
            pass
        self.cur_line += 1
        self.stdscr.refresh()

    def reset(self):
        if self.dummy:
            return
        # mark the last line we write
        # try:
        #     self.stdscr.move(self.cur_line, 0)
        #     self.stdscr.clrtoeol()
        # except curses.error:
        #     # The window size may be smaller than you want
        #     pass
        self.cur_line = 0
        self.stdscr.clear()

    def exit(self):
        if self.dummy:
            return
        # https://stackoverflow.com/a/18937214
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()


SP = StatusPrinter()
atexit.register(SP.exit)
