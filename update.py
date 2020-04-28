import os
import time

if os.path.exists("/home/pi/update"):
    try:
        remove = os.system("sudo rm -R /home/pi/sams_system")
        print(remove)
        clone = os.system("git clone https://github.com/anderswodenker/sams-app.git /home/pi/sams_system")
        print(clone)
        if clone == 0:
            remove_update = os.system("rm /home/pi/update")
            print(remove_update)
            done = os.system("touch /home/pi/done")
            print(done)
            time.sleep(5)
            os.system("sudo reboot")
    except Exception as e:
        print(e)
