import os
from shutil import copyfile


def update():
    try:
        print("copy")
        copyfile("/home/pi/sams_system/update.py", "/home/pi/update.py")
        os.system("python3 /home/pi/update.py")
    except Exception as e:
        print(e)


update()
