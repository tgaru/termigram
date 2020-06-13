#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from math import *
from services import settings, store, app
from builders import dialogs_builder

panel_x = None
panel_y = None
panel_width = None
panel_height = None


def init():
    global panel_x, panel_y, panel_width, panel_height

    panel_x = 0
    panel_y = 0
    panel_height = store.window_height
    panel_width = ceil(store.window_width * 0.3)


def make():


    #store.panels.dialogs = panel_builder.box(panel_x, panel_y, panel_width, panel_height, 'Dialogs')
    dialogs_builder.build(panel_x, panel_y, panel_width, panel_height)


async def key_handler(key):
    if key == curses.KEY_DOWN:
        store.dialogs_position = min(len(store.dialogs) - 2, store.dialogs_position + 1)

    if key == curses.KEY_UP:
        store.dialogs_position = max(0, store.dialogs_position - 1)

    if key == curses.KEY_RIGHT:
        await app.open_dialog(store.dialogs[store.dialogs_position])
        store.chat.messages_position = 0
        store.active_panel = 'messages'
