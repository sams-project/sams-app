import os
import shutil
import mapping


class SelfChecker:
    def __init__(self):
        # todo:
        # check all .ini files
        # check internet connection
        # check sensors
        # create summary
        self.summary = {}

    @staticmethod
    def check_files():
        summary_files = {}
        for file in mapping.files:
            nothing, home_folder, user, important_file = file.split("/")
            if not os.path.exists(file):
                shutil.copyfile(f"/home/pi/sams_system/{summary_files[important_file]}", f"/home/pi/{summary_files[important_file]}")
                summary_files[important_file] = False

        return summary_files

    def check_connection(self):
        pass

    def check_sensors(self):
        pass

    def self_check(self):
        pass