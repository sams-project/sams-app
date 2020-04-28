import os

try:
    if not os.path.exists("/home/pi/done"):
        remove = os.system("sudo rm -R /home/pi/sams_system")
        print(remove)
        clone = os.system("git clone https://github.com/anderswodenker/sams-app.git /home/pi/sams_system")
        if clone == 0:
            del_update = os.system("rm /home/pi/update")
            os.system("sudo touch /home/pi/done")
            print(del_update)
            os.system("sudo reboot")
except Exception as e:
    print(e)
