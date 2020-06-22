import requests
from main.configuration.token_config import TokenConfig
from main.helper.wifi_helper import WifiHelper
import mapping
import time


class DataApi:
    def __init__(self):
        self.token_config = TokenConfig()
        self.wifi_helper = WifiHelper()

    # get header with valid token
    def get_header(self):
        token_data = self.token_config.read_token()
        header = {
            'content-type': 'application/json',
            'Authorization': token_data["token"]
        }
        return header

    #  send dataset
    def send_data(self, dataset):
        time.sleep(5)  # wait 5 seconds to prevent response error
        try:
            resp = requests.post(
                mapping.dwh_data,
                json=dataset,
                headers=self.get_header()
            )

            if resp.status_code == 200:  # Dataset OK
                self.wifi_helper.update_online_status(True)
                return True
            if resp.status_code == 400:  # 400 (Dataset corrupted)
                return "delete"

        except Exception:
            self.wifi_helper.update_online_status(False)
            return False

    # get hardware configuration
    def get_config(self):
        try:
            config = requests.get(
                mapping.dwh_config,
                headers=self.get_header()
            )

            if config.status_code == 200:
                return config
            else:
                return False
        except Exception:
            return False
