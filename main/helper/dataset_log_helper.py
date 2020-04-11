import json
import os
import mapping
import psutil
from main.dwh.data_api import DataApi
from main.dwh.log_message import send_log
from main.configuration.local_config import LocalConfig


class DatasetLogHelper:
    def __init__(self):
        self.log_path = mapping.app_log
        self.data_api = DataApi()
        self.config = LocalConfig()
        self.files = os.listdir(self.log_path)
        self.dataset_corrupted_counter = 0

    def insert(self, json_data):
        files = os.listdir(self.log_path)
        if range(len(files)) != 0:
            file = int(
                len([name for name in os.listdir(self.log_path) if
                     os.path.isfile(os.path.join(self.log_path, name))])) + 1
        else:
            file = int(1)
        try:
            path = '/'
            bytes_avail = psutil.disk_usage(path).free
            gigabytes_avail = bytes_avail / 1024 / 1024 / 1024

            if gigabytes_avail >= 0.5:
                with open(self.log_path + str(file) + ".json", 'w') as f:
                    json.dump(json_data, f)
                    f.close()

            else:
                send_log("No more space available: {} GB".format(round(gigabytes_avail, 2)), "warning")
                files = []
                for name in os.listdir(self.log_path):
                    file_number = name.replace(".json", "")
                    files.append(int(file_number))

                files.sort()
                for logfile in files:
                    if int(logfile) % 2:
                        pass
                    else:
                        last_number = files[-1]
                        last_number = int(last_number) + 1
                        with open(self.log_path + str(last_number) + ".json", 'w') as f:
                            json.dump(json_data, f)
                            f.close()
                        os.remove(self.log_path + str(logfile) + ".json")
                        break

        except Exception as e:
            send_log("Failed to insert log files: ".format(e), "error")

    def list_dir(self):
        self.files = os.listdir(self.log_path)
        self.files.sort()

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path) as json_file:
                file_data = json.load(json_file)
            return file_data
        except Exception as e:
            send_log("Failed to read log files: ".format(e), "error")
            return False

    def has_log_files(self):
        if not os.listdir(self.log_path):
            return False
        else:
            return True

    def post_log_files(self):
        try:
            post_logs = self.has_log_files()  # check if app has log files
            while post_logs:
                self.list_dir()
                for x in self.files:
                    file = self.read_file(self.log_path + str(x))
                    response = self.data_api.send_data(file)
                    if response:
                        os.remove(self.log_path + str(x))  # delete file
                        post_logs = self.has_log_files()  # ask for more log files
                    if response == "delete":
                        send_log("File corrupted! Delete file", "warning")
                        self.dataset_corrupted_counter += 1
                        os.remove(self.log_path + str(x))
                        post_logs = self.has_log_files()
                    if not response:
                        post_logs = False

            return True

        except Exception as e:
            send_log("Failed to post log files: ".format(e), "error")
            return False
