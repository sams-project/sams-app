import shutil
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
            clone = os.system("sudo git clone https://github.com/sams-project/sams-app.git /home/pi/sams_system")
            if clone == 0:
                return True
            else:
                return False
        except Exception:
            return False

    def update(self):
        try:
            if self.start:
                if self.del_directory():
                    cloning = self.clone_directory()
                    if cloning:
                        self.config.set("DEFAULT", "update", "0")
                        with open(self.path, 'w') as configfile:
                            self.config.write(configfile)
                        os.system("sudo chown pi:pi -R /home/pi/sams_system")
                        time.sleep(60)
                        os.system('sudo reboot')
        except Exception:
            pass


updater = Updater()
updater.update()
