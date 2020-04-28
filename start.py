from main.application import Application

app = Application()

if app.app_config.local_config.start:
    app.start()
