from main.application import Application
from main.configuration.local_config import LocalConfig
import os

conf = LocalConfig()

if conf.start:
    if not os.path.exists("/home/pi/update"):
        app = Application()
        app.start()
    else:
        remove = os.system("sudo rm -R /home/pi/sams_system")
        print(remove)
        clone = os.system("git clone https://github.com/anderswodenker/sams-app.git /home/pi/sams_system")
        print(clone)
        del_update = os.system("rm /home/pi/update")
        print(del_update)
        os.system("sudo reboot")
