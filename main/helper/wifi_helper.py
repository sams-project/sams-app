import rssi
import os
from main.configuration.local_config import LocalConfig


class WifiHelper:
    def __init__(self):
        self.interface = 'wlan0'
        self.rssi_scanner = rssi.RSSI_Scan(self.interface)
        self.local_config = LocalConfig()

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

    def online_status(self):
        try:
            response = os.system("ping -c 2 " + "google.com")
            if response == 0:
                self.local_config.set_config_data("DEFAULT", "is_online", 1)
                return True
            else:
                self.local_config.set_config_data("DEFAULT", "is_online", 0)
                return False
        except Exception:
            return False
