import shutil
from git import Repo
import configparser
import os
import time


class Updater:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = "/home/pi/application.ini"
        self.config.read(self.path)
        self.start = self.config['DEFAULT'].getboolean('update')

    @staticmethod
    def del_directory():
        try:
            shutil.rmtree('/home/pi/sams_system', ignore_errors=True)
            return True
        except Exception:
            return False

    @staticmethod
    def clone_directory():
        try:
            Repo.clone_from("https://github.com/anderswodenker/sams-app.git", "sams_system")
            return True
        except Exception:
            return False

    def update(self):
        if self.start:
            if self.del_directory():
                if self.clone_directory():
                    self.config.set("DEFAULT", "update", "0")
                    with open(self.path, 'w') as configfile:
                        self.config.write(configfile)
                    time.sleep(60)
                    os.system('sudo reboot')


updater = Updater()
updater.update()

# v 2.3 !
