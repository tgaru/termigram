#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from classes.Panels import Panels
from classes.Chat import Chat

# systems
window_width = 0
window_height = 0
datetime_today = None
dates = {
    'today': None,
    'yesterday': None
}

# panels
panels = None
active_panel = 'dialogs'

# telegram
telegram = None
current_user = None
users = {}

# dialogs panel
dialogs = None
dialogs_position = 0

# messages panel
chat = None


def init():
    global panels, chat
    panels = Panels()
    chat = Chat()

    init_variables()


def init_variables():
    global window_height, window_width, datetime_today, date_today

    h, w = os.popen('stty size', 'r').read().split()
    window_width = max(int(w), 50)
    window_height = max(int(h), 15)

    datetime_today = datetime.today()
    dates['today'] = datetime_today.date()
    dates['yesterday'] = (datetime_today - timedelta(days=1)).date()
