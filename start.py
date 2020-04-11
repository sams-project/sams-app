from main.application import Application
import os

if not os.path.exists("/home/pi/update"):
    app = Application()
    app.start()
else:
    remove = os.system("sudo rm -R /home/pi/sams_system")
    print(remove)
    clone = os.system("git clone https://github.com/sams-project/monitor.git /home/pi/sams_system")
    print(clone)
    del_update = os.system("rm /home/pi/update")
    print(del_update)
    os.system("sudo reboot")
