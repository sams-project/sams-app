from main.application import Application
import os


app = Application()

if os.path.exists("/home/pi/done"):  # update is done -> delete update file
    os.system("sudo rm /home/pi/update.py")

if app.app_config.local_config.start:
    app.start()
