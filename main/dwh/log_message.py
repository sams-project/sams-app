import requests
import time
from main.configuration.token_config import TokenConfig
from main.configuration.local_config import LocalConfig
import mapping

token = TokenConfig()
config = LocalConfig()


def send_log(message, level):
    try:
        if config.is_online:
            # levels: error, warning, info, debug
            token_data = token.read_token()
            header = {
                'content-type': 'application/json',
                'Authorization': token_data["token"]
            }

            payload = {"message": str(message), "level": str(level)}
            time.sleep(8)  # wait to avoid a connection error
            if not config.debug and level == "debug":
                pass
            else:
                requests.post(mapping.dwh_log, headers=header, json=payload)

    except Exception as e:
        print(f'log failed: {e}')
        pass
