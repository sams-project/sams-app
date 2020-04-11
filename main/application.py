from main.dwh.log_message import send_log
from main.dataset import Dataset
from main.configuration.app_config import ApplicationConfig
from main.helper.wifi_helper import WifiHelper
from main.helper.dataset_log_helper import DatasetLogHelper
from main.dwh.data_api import DataApi
import time
import os
import requests
import mapping
from main.helper.time_helper import get_time


class Application:
    def __init__(self):
        self.dataset_helper = DatasetLogHelper()  # saving and sends the dataset
        self.dataset = Dataset()  # dataset for take sensor data
        self.app_config = ApplicationConfig()  # configuration data (on- and offline)
        self.wifi_helper = WifiHelper()  # gets signal strength for debug purpose
        self.attempts = 0
        self.dwh_api = DataApi()

        os.system(f"sudo timedatectl set-timezone {str(self.app_config.local_config.timezone)}")

        # send status:
        send_log(f'Start Application: {self.app_config.local_config.version}', "debug")
        time.sleep(8)
        send_log(f'Signal Strength: {self.wifi_helper.get_signal_strength()}', "debug")

    def start(self):
        while True:
            self.app_config.local_config.get_config_data()
            sensors = []
            try:
                self.app_config.sync_config()  # sync offline with online configuration

                if self.app_config.local_config.is_ds18b20:
                    sensors.append("DS18B20")  # TEMP SENSOR
                if self.app_config.local_config.is_dht22:
                    sensors.append("DHT22")  # TEMP and HUMIDITY SENSOR
                if self.app_config.local_config.is_scale:
                    sensors.append("SCALE")
                if self.app_config.local_config.is_microphone:
                    sensors.append("MICROPHONE")

                # START GET AND SEND DATASET BLOCK
                for sensor in sensors:
                    dataset = self.dataset.get_data(sensor)  # get dataset from sensor
                    if dataset:
                        for x in range(len(dataset)):
                            if not dataset[x] or not hasattr(dataset[x], '__len__'):
                                self.attempts += 1  # sensor is offline or sends no valid data
                                send_log(f'{sensor} failed!', "error")
                            else:
                                self.app_config.local_config.get_config_data()
                                if self.app_config.local_config.is_online:
                                    self.dwh_api.send_data(dataset[x])  # try to send dataset
                                    time.sleep(5)
                                else:
                                    self.dataset_helper.insert(dataset[x])  # save data

                    else:
                        self.attempts += 1  # sensor is offline or sends no valid data
                        send_log(f'{sensor} failed!', "error")

                # END DATASET BLOCK ###

                # START POST LOG FILES ####
                if self.app_config.local_config.is_online:
                    response = self.dataset_helper.post_log_files()
                    if not response:
                        self.attempts += 1
                # END POST LOG FILES ####

                # START CHECKING FAILED ATTEMPTS BLOCK
                if int(self.attempts) >= int(self.app_config.local_config.interval_attempts_before_restart):
                    self.restart_hive("Too many errors: reboot system!", "error")
                    # todo welcher sensor ist verantwortlich / in extra Datei speichern
                    # todo / in der App anzeigen / Sensor ueberspringen
                # END FAILED ATTEMPTS BLOCK ###

                # START CHECKING UPDATE
                if self.app_config.local_config.is_online and self.app_config.local_config.auto_update:
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

            if git_version > self.app_config.local_config.version:
                os.system("sudo touch /home/pi/update")
                self.app_config.local_config.set_config_data("DEFAULT", "version", git_version)
                self.restart_hive(f"Start Update from version: {old_version} to: {git_version}", "debug")
        except Exception:
            pass
