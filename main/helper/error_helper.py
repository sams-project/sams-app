import configparser
import mapping


class ErrorHelper:
    def __init__(self):
        self.path = mapping.sensor_errors
        self.config = configparser.ConfigParser()

    def get_sensor_data(self):
        self.config.read(self.path)
        errors = {}
        for key in self.config.items():
            if "DEFAULT" not in key:
                errors[key[0]] = {"errors": self.config[key[0]].get('errors'),
                                  "restarted": self.config[key[0]].get('restarted')}

        return errors

    def get_sensors_with_errors(self):
        sensor_data = self.get_sensor_data()
        errors = {}
        for sensors in sensor_data.items():
            if int(sensors[1]['errors']) >= 2 and int(sensors[1]['restarted']) >= 1:
                errors[sensors[0]] = "True"

        return errors

    def has_error(self, sensor):
        try:
            sensor_data = self.get_sensor_data()
            for sensors in sensor_data.items():
                if sensor == str(sensors[0]):
                    if int(sensors[1]['errors']) >= 2 and int(sensors[1]['restarted']) >= 1:
                        return True
                    else:
                        return False
        except Exception as e:
            print(e)

    def set_sensor_with_error(self, sensor):
        self.config.read(self.path)
        for key in self.config.items():
            if str(key[0]) == sensor:
                error_count = int(self.config[key[0]].get("errors"))
                error_count += 1
                self.config.set(key[0], "errors", str(error_count))
                self.write_config()

    def set_sensor_restarted(self, sensor):
        self.config.read(self.path)
        for key in self.config.items():
            if str(key[0]) == sensor:
                error_count = int(self.config[key[0]].get("restarted"))
                error_count += 1
                self.config.set(key[0], "restarted", str(error_count))
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
