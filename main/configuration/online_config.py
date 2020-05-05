import json
from main.dwh.data_api import DataApi
import mapping
import os


class OnlineConfig:
    def __init__(self):
        self.sams_dwh = DataApi()
        self.response = ""
        self.groupname = ""
        self.version = ""
        self.is_dht22 = False
        self.is_scale = True
        self.is_microphone = True
        self.is_ds18b20 = True
        self.interval_median = ""
        self.interval_app_wait_seconds = 0
        self.interval_attempts_before_restart = 0
        self.dht22_pin = 0
        self.audio_duration = 0
        self.audio_fs = 0
        self.auto_update = 0
        self.auto_shutdown = 0
        self.debug = 0
        self.timezone = ""

    def get_config_data(self):
        try:
            json_data = self.sams_dwh.get_config()
            if json_data:
                data = json.loads(json_data.content.decode('utf-8'))
                self.groupname = data['group']['name']
                self.is_dht22 = data['group']['is_dht22']
                self.auto_update = data['group']['auto_update']
                self.auto_shutdown = data['group']['auto_shutdown']
                self.debug = data['group']['debug']
                self.is_scale = data['group']['is_scale']
                self.is_microphone = data['group']['is_microphone']
                self.is_ds18b20 = data['group']['is_ds18b20']
                self.interval_median = data['group']['app_median']
                self.interval_app_wait_seconds = data['group']['app_wait_seconds']
                self.interval_attempts_before_restart = data['group']['app_attempts_before_restart']
                self.dht22_pin = data['group']['dht22_pin']
                self.audio_duration = data['group']['audio_duration']
                self.audio_fs = data['group']['audio_fs']
                self.timezone = data['group']['timezone']

                try:
                    if not os.path.exists(mapping.app_witty_pi):
                        os.system(f'touch {mapping.app_witty_pi}')
                    with open(str(mapping.app_witty_pi), "w+") as filehandler:
                        filehandler.writelines(data['group']['wittyPi'])

                    if not os.path.exists(mapping.witty_pi):
                        os.system(f'touch {mapping.witty_pi}')
                    with open(str(mapping.witty_pi), "w+") as filehandler:
                        filehandler.writelines(data['group']['wittyPi'])
                except Exception:
                    os.system(f'rm {mapping.app_witty_pi}')
                    os.system(f'rm {mapping.witty_pi}')
                    pass

                return True

        except Exception as e:
            print(e)
            return False
