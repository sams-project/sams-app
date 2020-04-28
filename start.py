from main.application import Application
import os

app = Application()

if app.app_config.local_config.start:
    app.start()
