#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import emoji
import re
from wcwidth import wcswidth
from panels import screen, dialogs, messages, input, chattop
from services import store, app
from classes import Panels


def curses_init():
    store.panels.screen = curses.initscr()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.curs_set(0)
    store.panels.screen.keypad(1)
    store.panels.screen.nodelay(1)


def panels_init():
    screen.init()
    dialogs.init()
    messages.init()
    input.init()
    chattop.init()


def render():
    screen.make()
    dialogs.make()
    messages.make()
    input.make()
    chattop.make()

    store.panels.screen.refresh()
    store.panels.dialogs.refresh()
    store.panels.messages.refresh()
    store.panels.input.refresh()
    store.panels.chattop.refresh()


async def key_handler(key):
    await globals()[store.active_panel].key_handler(key)


async def open_dialog(dialog_ident, focus=True):
    store.chat.entity = await store.telegram.get_entity(dialog_ident)
    store.chat.type = store.chat.entity.__class__.__name__
    store.chat.id = int('-100' + str(store.chat.entity.id)) if store.chat.type == 'Channel' else store.chat.entity.id
    store.chat.messages = await store.telegram.get_messages(store.chat.entity, 20)

    if store.chat.messages:
        for m in store.chat.messages:
            if m.sender_id not in store.users:
                store.users[m.sender_id] = m.sender

    store.chat.messages_offset = 0
    store.chat.messages_position = 0

    if focus:
        store.active_panel = 'messages'


def close_dialog():
    store.chat.__init__()


def format_text(text):
    return re.sub(emoji.get_emoji_regexp(), '[?]', text)


def splice(text, length, spaces=True):
    result = ''
    counter = 0

    for char in text:
        add_sum = wcswidth(char)

        if counter + add_sum > length:
            break

        result += char
        counter += add_sum

    if spaces:
        result += ''.ljust(length-counter)

    return result


def shorten(text, length):
    return splice(text, length, spaces=False)


def ljust(text, width):
    needed = width - wcswidth(text)

    if needed > 0:
        return text + ' ' * needed
    else:
        return text


def datetime_to_local(d):
    return d.replace(tzinfo=d.tzinfo).astimezone(tz=None)


def ender():
    curses.endwin()
