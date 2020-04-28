from main.application import Application
from main.configuration.local_config import LocalConfig
import os
from shutil import copyfile


conf = LocalConfig()

if conf.start:
    if os.path.exists("/home/pi/done"):
        del_update = os.system("rm /home/pi/update.py")

    if not os.path.exists("/home/pi/update"):
        app = Application()
        app.start()
    else:
        try:
            copyfile("/home/pi/sams_system/update.py", "/home/pi/update.py")
            os.system("sudo reboot")
        except Exception as e:
            print(e)
