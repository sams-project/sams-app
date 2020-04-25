import configparser
import mapping


class ErrorHelper:
    def __init__(self):
        self.path = mapping.sensor_errors
        self.config = configparser.ConfigParser()

    def get_sensor_with_error(self):
        self.config.read(self.path)
        errors = {}
        for key in self.config.defaults():
            if int(self.config['DEFAULT'].get(key)) > 2:  # two errors from the same sensor between 2 reboots
                errors[key] = self.config['DEFAULT'].get(key)

        return errors

    def has_error(self, sensor):
        errors = self.get_sensor_with_error()
        for error in errors:
            if error == sensor:
                return True

        return False

    def set_sensor_with_error(self, sensor):
        self.config.read(self.path)
        for key in self.config.defaults():
            if str(key) == sensor:
                error_count = int(self.config['DEFAULT'].get(key))
                error_count += 1
                self.config.set("DEFAULT", str(key), str(error_count))
                self.write_config()

    def reset_errors(self):
        for key in self.config.defaults():
            self.config.set("DEFAULT", str(key), str(0))
        self.write_config()

    def write_config(self):
        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)
        except IOError:
            pass
