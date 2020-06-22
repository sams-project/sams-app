import requests
from main.configuration.user_config import UserConfig
from main.configuration.token_config import TokenConfig
from main.helper.time_helper import get_diff_seconds
import mapping


class TokenHandler:
    def __init__(self):
        self.user_config = UserConfig()
        self.token_config = TokenConfig()
        self.expires_in = 0
        self.auth = {}
        self.known_error = "Failed to establish a new connection"

        self.token_dataset = {
            "client_id": self.user_config.client_id,
            "client_secret": self.user_config.client_secret,
            "audience": "sams-dwh-web-api",
            "grant_type": "client_credentials"
        }

    def get_access_token(self):
        if self.is_expired():
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
                self.token_config.reset_token()
                return False

    def is_expired(self):
        token_data = self.token_config.read_token()
        last_token = token_data["last_token"]
        expires_in = token_data["expires_in"]
        error = token_data["token_error"]
        if self.known_error in error:
            # todo reset config und stell sicher dass nur ein weiteres mal versucht wird eine Verbindung aufzubauen
            pass


        if last_token != "":
            diff = get_diff_seconds(last_token)
            if diff >= float(expires_in):
                return True  # token is expired
            else:
                return False  # token is valid
        else:
            return True  # no valid token in token.ini
