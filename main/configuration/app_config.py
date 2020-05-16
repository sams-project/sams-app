from main.configuration.local_config import LocalConfig
from main.configuration.online_config import OnlineConfig
from main.dwh.log_message import send_log


class ApplicationConfig:
    def __init__(self):
        self.local_config = LocalConfig()
        self.online_config = OnlineConfig()

    def sync_config(self):
        try:
            if self.online_config.get_config_data():
                self.local_config.set_config_data("DEFAULT", "group", self.online_config.groupname)
                self.local_config.set_config_data("DEFAULT", "ignore_error", self.online_config.ignore_error)
                self.local_config.set_config_data("DEFAULT", "is_dht22", self.online_config.is_dht22)
                self.local_config.set_config_data("DEFAULT", "is_scale", self.online_config.is_scale)
                self.local_config.set_config_data("DEFAULT", "is_microphone", self.online_config.is_microphone)
                self.local_config.set_config_data("DEFAULT", "is_ds18b20", self.online_config.is_ds18b20)
                self.local_config.set_config_data("DEFAULT", "auto_update", self.online_config.auto_update)
                self.local_config.set_config_data("DEFAULT", "auto_shutdown", self.online_config.auto_shutdown)
                self.local_config.set_config_data("DEFAULT", "timezone", self.online_config.timezone)
                self.local_config.set_config_data("DEFAULT", "debug", self.online_config.debug)
                self.local_config.set_config_data("INTERVAL", "median", self.online_config.interval_median)
                self.local_config.set_config_data("INTERVAL", "app_wait_seconds",
                                                  self.online_config.interval_app_wait_seconds)
                self.local_config.set_config_data("INTERVAL", "attempts_before_restart",
                                                  self.online_config.interval_attempts_before_restart)
                self.local_config.set_config_data("DHT22", "dht22_pin", self.online_config.dht22_pin)
                self.local_config.set_config_data("AUDIO", "duration", self.online_config.audio_duration)
                self.local_config.set_config_data("AUDIO", "fs", self.online_config.audio_fs)

            if self.local_config.get_config_data():
                return True
            else:
                return False

        except Exception as e:
            send_log("Sync config Error: {}".format(e), "warning")
