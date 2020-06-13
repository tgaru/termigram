#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import textwrap
from math import *
from services import settings, store, styles

panel_x = None
panel_y = None
panel_width = None
panel_height = None


def init():
    global panel_x, panel_y, panel_width, panel_height

    panel_x = ceil(store.window_width * 0.3)
    panel_width = store.window_width - panel_x
    panel_height = 3
    panel_y = store.window_height - panel_height


def make():
    store.panels.input = curses.newwin(panel_height, panel_width, panel_y, panel_x)

    if not store.chat.entity:
        return

    store.panels.input.border(
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        curses.ACS_HLINE,
        ' ',
        curses.ACS_LTEE,
        curses.ACS_RTEE,
        curses.ACS_VLINE,
        curses.ACS_VLINE
    )

    store.panels.input.addstr(0, 1, 'Enter message', styles.green)


async def key_handler():
    pass
