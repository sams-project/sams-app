#!/usr/bin/env python3

from main.application import Application

app = Application()

if app.app_config.local_config.start and not app.app_config.local_config.is_update:
    try:
        app.start()
    except Exception as e:
        print(e)
