import configparser
import mapping
from main.helper.time_helper import get_time


class TokenConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_data = self.config['DEFAULT']
        self.config.read(mapping.token_config)

    def read_token(self):
        self.config.read(mapping.token_config)
        token = self.config['DEFAULT']['token']
        last_token = self.config['DEFAULT']['last_token']
        expires_in = self.config['DEFAULT']['expires_in']

        return {"token": token, "last_token": last_token, "expires_in": expires_in}

    def read_token_error(self):
        self.config.read(mapping.token_config)
        error = self.config_data['token_error']
        return error

    def write_token(self, token, expires_in):
        self.config.set("DEFAULT", "token", token)
        self.config.set("DEFAULT", "last_token", get_time())
        self.config.set("DEFAULT", "expires_in", expires_in)
        self.write_config()

    def write_token_error(self, error):
        self.config.set("DEFAULT", "token_error", error)
        self.write_config()

    def reset_token(self):
        self.config.set("DEFAULT", "token", "")
        self.config.set("DEFAULT", "last_token", "")
        self.config.set("DEFAULT", "expires_in", "")
        self.write_config()

    def write_config(self):
        try:
            with open(mapping.token_config, 'w') as configfile:
                self.config.write(configfile)
        except IOError:
            pass
