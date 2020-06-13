#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import datetime
from math import *
from services import styles, store, app
from wcwidth import wcswidth


def build(x, y, width, height):
    store.panels.messages = curses.newwin(height, width, y, x)

    if not store.chat.entity:
        store.panels.messages.addstr(floor(height/2), 1,  'Choose a dialogue'.center(width - 2), styles.yellow)
        return

    store.panels.messages.border(
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        ' ',
        ' ',
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        curses.ACS_VLINE,
        curses.ACS_VLINE
    )

    if store.chat.type != 'User' and store.chat.type != 'Channel':
        store.panels.messages.addstr(floor(height/2), 1, 'Unable to open'.center(width-2), styles.default)
        return

    if not store.chat.messages:
        return

    messages_len = len(store.chat.messages)

    if messages_len == 0:
        store.panels.messages.addstr(floor(height / 2), 1, 'No messages :('.center(width - 2), styles.default)
        return

    _messages_format(width, height)
    _print(width, height)


def _print(width, height):
    max_rows = height - 1
    printed_lines = 0

    for i in store.chat.messages_formatted:
        if i < store.chat.messages_position:
            continue

        message_formatted = store.chat.messages_formatted[i]

        text_style = styles.default
        title_style = styles.green
        if store.active_panel == 'messages' and i == store.chat.messages_position:
            text_style = styles.selected
            title_style = styles.selected

        line_index = 0
        lines_len = len(message_formatted['lines'])
        for line in message_formatted['lines']:

            if printed_lines < store.chat.messages_offset:
                printed_lines += 1
                line_index += 1
                continue

            line_len = len(line)
            y = max_rows - printed_lines + store.chat.messages_offset

            if y <= 0:
                break

            if message_formatted['from_me']:
                store.panels.messages.addstr(y, (width - line_len) - 1, str(line), text_style)
            else:
                store.panels.messages.addstr(y, 1, str(line), text_style)

                if line_index == lines_len - 1:
                    store.panels.messages.addstr(y, 2, message_formatted['title'], title_style)

            if line_index == 0:
                message_datetime = message_formatted['datetime'].strftime('%Y.%m.%d %H:%M')
                if message_formatted['datetime'].date() == store.dates['today']:
                    message_datetime = message_formatted['datetime'].strftime('%H:%M')
                elif message_formatted['datetime'].date() == store.dates['yesterday']:
                    message_datetime = message_formatted['datetime'].strftime('yesterday at %H:%M')

                message_datetime_len = len(message_datetime)
                x = line_len - message_datetime_len

                if message_formatted['from_me']:
                    x = width - message_datetime_len - 2

                x = max(x, 0)

                store.panels.messages.addstr(y, x, message_datetime, text_style)

            printed_lines += 1
            line_index += 1


def _messages_format(width, height):
    i = 0
    for m in store.chat.messages:
        if i in store.chat.messages_formatted:
            continue

        message_type = m.__class__.__name__

        if message_type != 'Message':
            continue

        message = app.format_text(m.message)
        message_user = store.users[m.from_id] if m.from_id in store.users else None

        n = width - ceil(width*0.2)
        msg_len = len(message)
        if msg_len < n:
            n = msg_len

        n = max(n, 20)

        store.chat.messages_formatted[i] = {
            'lines': [],
            'from_me': store.current_user.id == m.from_id,
            'title': app.shorten(str(message_user.first_name), 15) if message_user else '',
            'datetime': app.datetime_to_local(m.date)
        }

        store.chat.messages_formatted[i]['lines'].append('└' + ''.ljust(n, '─') + '┘')

        brs = message.split('\n')
        lines = []

        for br in brs:
            words = br.split(' ')
            line = ''

            for word in words:
                if wcswidth(line + word) <= n:
                    line += word + ' '
                else:
                    lines = ['│' + app.ljust(line.strip(), n) + '│'] + lines
                    line = ''

            if line != '':
                lines = ['│' + app.ljust(line.strip(), n) + '│'] + lines

        store.chat.messages_formatted[i]['lines'] += lines

        if store.chat.messages_formatted[i]['from_me']:
            store.chat.messages_formatted[i]['lines'].append('┌' + ''.ljust(n, '─') + '┬')
        else:
            store.chat.messages_formatted[i]['lines'].append('┬' + ''.ljust(n, '─') + '┐')

        i += 1
