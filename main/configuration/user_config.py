import configparser
import mapping


class UserConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(mapping.user_config)
        self.client_id = self.config["DEFAULT"].get("client_id")
        self.client_secret = self.config["DEFAULT"].get("client_secret")

    def get_user_data(self):
        self.config.read(mapping.user_config)
        user_data = {}
        for key in self.config.defaults():
            user_data[key] = self.config["DEFAULT"].get(key)

        if user_data["client_id"] != "":
            return user_data
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
