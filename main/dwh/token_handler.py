import requests
import time
from main.configuration.user_config import UserConfig
from main.configuration.token_config import TokenConfig
from main.helper.time_helper import get_diff_seconds
from main.helper.wifi_helper import WifiHelper
import mapping
from main.dwh.log_message import send_log


class TokenHandler:
    def __init__(self):
        self.user_config = UserConfig()
        self.token_config = TokenConfig()
        self.wifi_helper = WifiHelper()
        self.expires_in = 0
        self.auth = {}

        self.token_dataset = {
            "client_id": self.user_config.client_id,
            "client_secret": self.user_config.client_secret,
            "audience": "sams-dwh-web-api",
            "grant_type": "client_credentials"
        }

    def get_access_token(self):
        token_data = self.token_config.read_token()
        if token_data["expires_in"] == "" or self.get_difference():
            try:
                self.auth = requests.post(
                    mapping.dwh_token,
                    json=self.token_dataset,
                    headers={'content-type': "application/json"}
                ).json()

                if 'error' in self.auth:
                    self.token_config.write_token_error(str(self.auth['error']))
                    return False
                else:
                    token = self.auth['token_type'] + ' ' + self.auth['access_token']
                    expires = self.auth['expires_in']
                    self.token_config.write_token(token, str(expires))
                    return True
            except Exception as e:
                self.token_config.write_token_error(str(e))
                return False

    def get_difference(self):
        token_data = self.token_config.read_token()
        last_token = token_data["last_token"]
        expires_in = token_data["expires_in"]

        if 'last_token' in token_data:
            diff = get_diff_seconds(last_token)
            if diff >= int(expires_in):
                return True
            else:
                return False
        else:
            return False

    def handle_token(self):
        try:
            self.get_access_token()
            while True:
                try:
                    if self.wifi_helper.online_status() and self.get_difference():
                        self.get_access_token()
                except Exception as e:
                    print(e)
                time.sleep(30)
        except Exception as e:
            send_log(f'Handle token error: {e}', "error")
