import configparser
import mapping


class UserConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(mapping.user_config)
        self.config_data = self.config['DEFAULT']
        self.client_id = self.config_data['client_id']
        self.client_secret = self.config_data['client_secret']

    def get_user_data(self):
        self.config.read(mapping.user_config)
        self.config_data = self.config['DEFAULT']
        self.client_id = self.config_data['client_id']
        self.client_secret = self.config_data['client_secret']
        data = {"user": self.client_id, "secret": self.client_secret}
        if data['user'] != "":
            return data
        else:
            return False

    def write_user_data(self, user, secret):
        self.config.set("DEFAULT", "client_id", str(user))
        self.config.set("DEFAULT", "client_secret", str(secret))
        try:
            with open(mapping.user_config, 'w') as configfile:
                self.config.write(configfile)
        except IOError:
            pass