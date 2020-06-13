#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import os
from dotenv import load_dotenv

telegram_api_key = None
telegram_api_hash = None


def init():
    global telegram_api_key, telegram_api_hash

    load_dotenv()
    telegram_api_key = os.getenv('TELEGRAM_API_KEY')
    telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
