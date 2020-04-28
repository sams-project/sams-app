from main.dwh.log_message import send_log
from main.dataset import Dataset
from main.configuration.app_config import ApplicationConfig
from main.helper.wifi_helper import WifiHelper
from main.helper.dataset_log_helper import DatasetLogHelper
from main.dwh.data_api import DataApi
from main.dwh.token_handler import TokenHandler
from main.helper.error_helper import ErrorHelper
from main.helper.time_helper import get_time
from main.helper.time_helper import set_timezone

import time
import os
import requests
import mapping

# v.2.4


class Application:
    def __init__(self):
        self.dataset_helper = DatasetLogHelper()  # saving and sends the dataset
        self.dataset = Dataset()  # dataset for take sensor data
        self.app_config = ApplicationConfig()  # configuration data (on- and offline)
        self.wifi_helper = WifiHelper()  # gets signal strength for debug purpose
        self.attempts = 0
        self.dwh_api = DataApi()
        self.token_handler = TokenHandler()
        self.error_helper = ErrorHelper()
        self.failed_sensor = ""

        self.token_handler.get_access_token()
        self.wifi_helper.update_online_status(False)

        # send status:
        send_log(f'Start Application: {self.app_config.local_config.version}', "debug")
        send_log(f'Signal Strength: {self.wifi_helper.get_signal_strength()}', "debug")
        set_timezone(self.app_config.local_config.timezone)
        for failed_sensor in self.error_helper.get_sensor_with_error():
            send_log(f'Please check {failed_sensor} and reset all errors to reactivate the sensor.', "warning")

    def start(self):
        while True:
            self.token_handler.get_access_token()

            if self.wifi_helper.is_online():
                self.app_config.sync_config()
            else:
                self.app_config.local_config.get_config_data()
            sensors = []
            try:
                if self.app_config.local_config.is_ds18b20 and not self.error_helper.has_error("ds18b20"):
                    sensors.append("ds18b20")  # TEMP SENSOR
                if self.app_config.local_config.is_dht22 and not self.error_helper.has_error("dht22"):
                    sensors.append("dht22")  # TEMP and HUMIDITY SENSOR
                if self.app_config.local_config.is_scale and not self.error_helper.has_error("scale"):
                    sensors.append("scale")
                if self.app_config.local_config.is_microphone and not self.error_helper.has_error("microphone"):
                    sensors.append("microphone")

                # START GET AND SEND DATASET BLOCK
                for sensor in sensors:
                    print(f'get sensor: {sensor}')
                    dataset = self.dataset.get_data(sensor)  # get dataset from sensor
                    if dataset:
                        for x in range(len(dataset)):
                            if not dataset[x] or not hasattr(dataset[x], '__len__'):
                                self.attempts += 1  # sensor is offline or sends no valid data
                                self.failed_sensor = str(sensor)
                                send_log(f'{sensor} failed!', "error")
                            else:
                                response = self.dwh_api.send_data(dataset[x])
                                if not response:
                                    self.dataset_helper.insert(dataset[x])  # save data
                    else:
                        self.attempts += 1  # sensor is offline or sends no valid data
                        self.failed_sensor = str(sensor)
                        send_log(f'{sensor} failed!', "error")

                # END DATASET BLOCK ###

                # START POST LOG FILES ####
                if self.wifi_helper.is_online():
                    response = self.dataset_helper.post_log_files()
                    if not response:
                        self.attempts += 1
                # END POST LOG FILES ####

                # START CHECKING FAILED ATTEMPTS BLOCK
                if int(self.attempts) >= int(self.app_config.local_config.interval_attempts_before_restart):
                    self.error_helper.set_sensor_with_error(self.failed_sensor)
                    self.restart_hive("Too many errors: reboot system!", "error")
                # END FAILED ATTEMPTS BLOCK ###

                # START CHECKING UPDATE
                if self.wifi_helper.is_online() and self.app_config.local_config.auto_update:
                    self.update()
                # END CHECKING UPDATE

                # START AUTO SHUTDOWN BLOCK
                if self.app_config.local_config.auto_shutdown:
                    send_log(f'Power off. System time: {str(get_time())}', "debug")
                    time.sleep(30)
                    os.system("sudo poweroff")
                # END AUTO SHUTDOWN BLOCK ###

                # WAIT BEFORE TAKE NEW DATASET
                time.sleep(int(self.app_config.local_config.interval_app_wait_seconds))
                # END WAIT ###

            except Exception as e:
                print(f'app crashed: {e}')
                self.restart_hive(f'Application crashed! Error: {e}. Reboot System', "error")

    @staticmethod
    def restart_hive(message, level):
        send_log(message, level)
        time.sleep(120)
        os.system('sudo reboot')

    def update(self):
        try:
            r = requests.get(mapping.version_url)
            git_version = r.content.decode("utf-8")
            old_version = self.app_config.local_config.version

            if r.status_code == 200:
                if git_version > self.app_config.local_config.version:
                    pull = os.system("git pull origin master")
                    if pull == 0:
                        self.restart_hive(f"update from {old_version} to {git_version}", "debug")
        except Exception as e:
            print(e)
