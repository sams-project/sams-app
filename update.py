import os

if os.path.exists("/home/pi/update"):
    try:
        stopping = os.system("sudo supervisorctl stop all")
        if stopping == 0:
            remove = os.system("sudo rm -R /home/pi/sams_system")
            print(remove)
            clone = os.system("git clone https://github.com/anderswodenker/sams-app.git /home/pi/sams_system")
            if clone == 0:
                print("restart all...")
                stopping = os.system("sudo supervisorctl restart all")
                os.system("touch /home/pi/done")
    except Exception as e:
        print(e)
