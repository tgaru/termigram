#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import curses
import textwrap
from math import *
from services import settings, store, app, styles
from telethon import utils
from builders import messages_builder
from wcwidth import wcswidth

panel_x = None
panel_y = None
panel_width = None
panel_height = None


def init():
    global panel_x, panel_y, panel_width, panel_height

    panel_x = ceil(store.window_width * 0.3)
    panel_y = 2
    panel_width = store.window_width - panel_x
    panel_height = store.window_height - 5


def make():
    messages_builder.build(panel_x, panel_y, panel_width, panel_height)


async def key_handler(key):
    if key == curses.KEY_UP:
        if store.chat.messages_position not in store.chat.messages_formatted or \
                'lines' not in store.chat.messages_formatted[store.chat.messages_position]:
            return

        message_rows = len(store.chat.messages_formatted[store.chat.messages_position]['lines'])
        hidden_rows = message_rows - panel_height + 2 - store.chat.messages_offset

        if hidden_rows > 0:
            store.chat.messages_offset += 3
        else:
            new_position = min(len(store.chat.messages) - 1, store.chat.messages_position + 1)
            if new_position not in store.chat.messages_formatted[store.chat.messages_position]:
                return

            store.chat.messages_position = new_position
            store.chat.messages_offset = 0

    if key == curses.KEY_DOWN:
        if store.chat.messages_offset > 0:
            store.chat.messages_offset -= 3
        else:
            store.chat.messages_position = max(0, store.chat.messages_position - 1)
            store.chat.messages_offset = 0

    if key == curses.KEY_LEFT:
        store.active_panel = 'dialogs'
        app.close_dialog()
