#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import telethon
import textwrap
from math import *
from services import settings, store, styles, app

panel_x = None
panel_y = None
panel_width = None
panel_height = None


def init():
    global panel_x, panel_y, panel_width, panel_height

    panel_x = ceil(store.window_width * 0.3)
    panel_width = store.window_width - panel_x
    panel_height = 3
    panel_y = 0


def make():
    store.panels.chattop = curses.newwin(panel_height, panel_width, panel_y, panel_x)

    if not store.chat.entity:
        return

    store.panels.chattop.border(
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        ' ',
        curses.ACS_HLINE,
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        curses.ACS_LTEE,
        curses.ACS_RTEE
    )

    title = app.splice(telethon.utils.get_display_name(store.chat.entity), 20)
    online_status = ''
    online_status_indicator = ['', styles.default]

    if store.chat.id in store.users and hasattr(store.users[store.chat.id], 'status') and store.users[store.chat.id].status:
        online_status_indicator = ['●', styles.red]

        user_status_type = store.users[store.chat.id].status.__class__.__name__

        if user_status_type == 'UserStatusRecently':
            online_status = 'last seen recently'
        elif user_status_type == 'UserStatusLastWeek':
            online_status = 'last seen a week ago'
        elif user_status_type == 'UserStatusLastMonth':
            online_status = 'last seen a month ago'
        elif user_status_type == 'UserStatusOffline':
            online_status = 'offline'
        elif user_status_type == 'UserStatusOnline':
            online_status = 'online'
            online_status_indicator = ['●', styles.green]

    online_status = app.splice(online_status, 20)

    store.panels.chattop.addstr(0, 2, title, styles.cyan)
    store.panels.chattop.addstr(1, 2, online_status_indicator[0], online_status_indicator[1])
    store.panels.chattop.addstr(1, 4, online_status, styles.default)


async def key_handler():
    pass
