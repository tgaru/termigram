#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
import emoji
import re
from wcwidth import wcswidth
from services import app, settings
from telethon import TelegramClient, events, sync

#telegram = TelegramClient('anon', settings.telegram_api_key, settings.telegram_api_hash)
#telegram.start()
#current_user = telegram.get_me()
#print(current_user)