import rssi
import configparser
import mapping


class WifiHelper:
    def __init__(self):
        self.interface = 'wlan0'
        self.rssi_scanner = rssi.RSSI_Scan(self.interface)
        self.config = configparser.ConfigParser()
        self.config.read(mapping.online_status)

    def get_signal_strength(self):
        ap_info = self.rssi_scanner.getAPinfo(sudo=True)
        signal = ap_info[0]['signal']
        strength = ""

        if signal > -50:
            strength = "excellent"
        if -50 >= signal > -60:
            strength = "ok"
        if -60 >= signal > -70:
            strength = "fair"
        if signal <= -70:
            strength = "weak"

        return strength

    def update_online_status(self, status):
        try:
            self.config.read(mapping.online_status)
            if status:
                self.config.set("DEFAULT", "is_online", str(1))
            else:
                self.config.set("DEFAULT", "is_online", str(0))
            self.write_config()

        except Exception:
            return False

    def is_online(self):
        self.config.read(mapping.online_status)
        return self.config['DEFAULT'].getboolean('is_online')

    def write_config(self):
        try:
            with open(mapping.online_status, 'w') as configfile:
                self.config.write(configfile)
        except IOError:
            pass
