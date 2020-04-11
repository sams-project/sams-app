import requests
from main.configuration.user_config import UserConfig
from main.configuration.token_config import TokenConfig
import mapping


class DataApi:
    def __init__(self):
        self.user_config = UserConfig()
        self.token_config = TokenConfig()

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
        try:
            resp = requests.post(
                mapping.dwh_data,
                json=dataset,
                headers=self.get_header()
            )

            if resp.status_code == 200:  # Dataset OK
                return True
            if resp.status_code == 400 or resp.status_code == 500:  # 400 or 500 (Dataset corrupted)
                return "delete"

        except Exception:
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
