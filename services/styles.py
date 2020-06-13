#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses

default = None
selected = None
green = None
yellow = None
blue = None
cyan = None
red = None
megenta = None

green_bg = None
white_bg = None


def init():
    global default, selected, green, yellow, blue, cyan, red, megenta
    global green_bg, white_bg

    default = curses.A_NORMAL
    selected = curses.color_pair(1)

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    green = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    yellow = curses.color_pair(3)

    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    blue = curses.color_pair(4)

    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    cyan = curses.color_pair(5)

    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    red = curses.color_pair(6)

    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    megenta = curses.color_pair(7)

    curses.init_pair(101, curses.COLOR_BLACK, curses.COLOR_GREEN)
    green_bg = curses.color_pair(101)

    curses.init_pair(102, curses.COLOR_BLACK, curses.COLOR_WHITE)
    white_bg = curses.color_pair(102)

