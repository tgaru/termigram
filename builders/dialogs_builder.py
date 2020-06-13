#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from math import *
from services import styles, store
from services import app


def build(x, y, width, height):
    store.panels.dialogs = curses.newwin(height, width, y, x)

    store.panels.dialogs.border(
        ' ',
        curses.ACS_VLINE,
        curses.ACS_HLINE,
        ' ',
        curses.ACS_HLINE,
        curses.ACS_URCORNER,
        ' ',
        curses.ACS_VLINE
    )

    store.panels.dialogs.addstr(0, 1, 'Dialogs', styles.green)

    dialogs_len = len(store.dialogs)
    max_rows = height - 1
    page = floor(store.dialogs_position / max_rows)
    offset_rows = page * max_rows

    if dialogs_len == 0:
        store.panels.dialogs.addstr(2, 0, 'No chats :(', styles.yellow)
        return

    for i in range(0, max_rows):
        dialog = store.dialogs[i + offset_rows]
        dialog_title = app.format_text(dialog.name)
        dialog_title = app.splice(dialog_title, width-1)

        if i + offset_rows < dialogs_len-1:
            style = styles.default

            if store.active_panel == 'dialogs' and store.dialogs_position == i + offset_rows:
                style = styles.selected
            elif store.chat.entity and store.chat.id == dialog.id:
                style = styles.green_bg

            store.panels.dialogs.addstr(i + 1, 0, dialog_title, style)
        else:
            break
