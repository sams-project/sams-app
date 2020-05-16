import configparser
import mapping


class LocalConfig:
    def __init__(self):
        self.path = mapping.app_config
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.config.sections()

        # DEFAULT
        self.start = self.config['DEFAULT'].getboolean('start')
        self.ignore_error = self.config['DEFAULT'].getboolean('ignore_error')
        self.is_update = self.config['DEFAULT'].getboolean('update')
        self.group = self.config['DEFAULT']['group']
        self.is_dht22 = self.config['DEFAULT'].getboolean('is_dht22')
        self.is_scale = self.config['DEFAULT'].getboolean('is_scale')
        self.is_microphone = self.config['DEFAULT'].getboolean('is_microphone')
        self.is_ds18b20 = self.config['DEFAULT'].getboolean('is_ds18b20')
        self.auto_update = self.config['DEFAULT'].getboolean('auto_update')
        self.auto_shutdown = self.config['DEFAULT'].getboolean('auto_shutdown')
        self.debug = self.config['DEFAULT'].getboolean('debug')
        self.is_online = self.config['DEFAULT'].getboolean('is_online')
        self.timezone = self.config['DEFAULT']['timezone']
        self.version = self.get_version()

        # SCALE
        self.scale_ratio = self.config['SCALE']['ratio']
        self.scale_offset = self.config['SCALE']['offset']
        self.scale_calibrated = self.config['SCALE'].getboolean('calibrated')

        # INTERVAL
        self.interval_median = self.config['INTERVAL']['median']
        self.interval_app_wait_seconds = self.config['INTERVAL']['app_wait_seconds']
        self.interval_attempts_before_restart = self.config['INTERVAL']['attempts_before_restart']

        # DHT 22
        self.dht22_pin = self.config['DHT22']['dht22_pin']

        # AUDIO
        self.audio_duration = self.config['AUDIO']['duration']
        self.audio_fs = self.config['AUDIO']['fs']

    def get_config_data(self):
        try:
            self.config.read(self.path)
            # DEFAULT
            self.group = self.config['DEFAULT']['group']
            self.ignore_error = self.config['DEFAULT'].getboolean('ignore_error')
            self.is_dht22 = self.config['DEFAULT'].getboolean('is_dht22')
            self.is_scale = self.config['DEFAULT'].getboolean('is_scale')
            self.is_microphone = self.config['DEFAULT'].getboolean('is_microphone')
            self.is_ds18b20 = self.config['DEFAULT'].getboolean('is_ds18b20')
            self.auto_update = self.config['DEFAULT'].getboolean('auto_update')
            self.auto_shutdown = self.config['DEFAULT'].getboolean('auto_shutdown')
            self.debug = self.config['DEFAULT'].getboolean('debug')
            self.is_online = self.config['DEFAULT'].getboolean('is_online')
            self.timezone = self.config['DEFAULT']['timezone']
            self.version = self.get_version()

            # SCALE
            self.scale_ratio = self.config['SCALE']['ratio']
            self.scale_offset = self.config['SCALE']['offset']
            self.scale_calibrated = self.config['SCALE'].getboolean('calibrated')

            # INTERVAL
            self.interval_median = self.config['INTERVAL']['median']
            self.interval_app_wait_seconds = self.config['INTERVAL']['app_wait_seconds']
            self.interval_attempts_before_restart = self.config['INTERVAL']['attempts_before_restart']

            # DHT 22
            self.dht22_pin = self.config['DHT22']['dht22_pin']

            # AUDIO
            self.audio_duration = self.config['AUDIO']['duration']
            self.audio_fs = self.config['AUDIO']['fs']

            return True
        except IOError:
            return False

    def set_config_data(self, section, key, value):
        self.config.set(section, key, str(value))
        self.write_config()

    @staticmethod
    def get_version():
        file = open(mapping.version_file, "r")
        version = file.read()
        file.close()
        return version

    def set_update(self):
        self.config.set("DEFAULT", "update", "1")
        self.write_config()

    def write_config(self):
        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)
        except IOError:
            pass
