#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import time
import curses
import os
import socks
import textwrap
import sys
from math import *
from services import settings, app, store, styles
from telethon import TelegramClient, events, sync


def init():
    store.init()
    settings.init()
    app.curses_init()
    app.panels_init()
    styles.init()

    store.telegram = TelegramClient('sessions/anon', settings.telegram_api_key, settings.telegram_api_hash)
    store.telegram.start()
    store.current_user = store.telegram.get_me()
    store.dialogs = store.telegram.get_dialogs()


async def rendering():
    while True:
        app.render()
        await asyncio.sleep(1 / 30)


async def key_handler():
    key = store.panels.screen.getch()
    while key != 27:
        await app.key_handler(key)
        key = store.panels.screen.getch()
        await asyncio.sleep(1 / 30)


async def sleep1s():
    while True:
        store.init_variables()
        app.panels_init()
        await asyncio.sleep(1)


init()

# while True:
#    app.render()
#    time.sleep(0.1)

loop = asyncio.get_event_loop()
loop.create_task(rendering())
loop.create_task(key_handler())
loop.create_task(sleep1s())

try:
    loop.run_forever()
except KeyboardInterrupt:
    curses.endwin()
    pass
