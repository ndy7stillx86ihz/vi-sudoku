import curses


class ColorPairs:
    NORMAL = 1
    FIXED = 2
    CURSOR = 3
    ERROR = 4
    CONFLICT = 5
    HEADER = 6
    INFO = 7
    CANDIDATE = 8


def init_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(ColorPairs.NORMAL, curses.COLOR_WHITE, -1)

    curses.init_pair(ColorPairs.FIXED, curses.COLOR_CYAN, -1)

    curses.init_pair(ColorPairs.CURSOR, curses.COLOR_BLACK, curses.COLOR_CYAN)

    curses.init_pair(ColorPairs.ERROR, curses.COLOR_RED, -1)

    curses.init_pair(ColorPairs.CONFLICT, curses.COLOR_YELLOW, -1)

    curses.init_pair(ColorPairs.HEADER, curses.COLOR_GREEN, -1)

    curses.init_pair(ColorPairs.INFO, curses.COLOR_CYAN, -1)

    curses.init_pair(ColorPairs.CANDIDATE, curses.COLOR_YELLOW, -1)
