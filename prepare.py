#  reset all credentials and prepare the system for production mode

import shutil
import mapping
import os


def prepare_all_files():
    shutil.copyfile("/home/pi/sams_system/application.ini", "/home/pi/application.ini")
    shutil.copyfile("/home/pi/sams_system/user.ini", "/home/pi/user.ini")
    shutil.copyfile("/home/pi/sams_system/token.ini", "/home/pi/token.ini")
    shutil.copyfile("/home/pi/sams_system/online.ini", "/home/pi/online.ini")
    shutil.copyfile("/home/pi/sams_system/error.ini", "/home/pi/error.ini")
    os.mkdir(mapping.app_log)
    print("done")


prepare_all_files()