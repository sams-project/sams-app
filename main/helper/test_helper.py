from main.dwh.token_handler import TokenHandler
from main.configuration.app_config import ApplicationConfig
from main.helper.microphone_helper import MicrophoneHelper
from main.dataset import Dataset
from main.helper.color import Color
import psutil


class AppTest:
    def __init__(self):
        self.token_handler = TokenHandler()
        self.app_config = ApplicationConfig()
        self.mic = MicrophoneHelper()
        self.dataset = Dataset()
        self.color_print = Color()
        self.sensors = []

        if self.app_config.local_config.is_dht22:
            self.sensors.append("dht22")
        if self.app_config.local_config.is_ds18b20:
            self.sensors.append("ds18b20")
        if self.app_config.local_config.is_scale:
            self.sensors.append("scale")

    def app_status(self):
        # liefert den aktuellen Status der App zurück
        # wieviele failed attempts
        # führt messung durch oder wartet
        # läuft oder läuft nicht
        pass

    def token_test(self):
        # liefert true wenn user credentials richtig und valides token erhalten
        pass

    def config_test(self):
        # liefert true wenn konfigurationsdatei ist da und kann mit dem dw synchronisiert werden
        pass

    @staticmethod
    def get_available_space():
        path = '/'
        bytes_avail = psutil.disk_usage(path).free
        gigabytes_avail = bytes_avail / 1024 / 1024 / 1024

        return round(gigabytes_avail, 2)

    def dataset_test(self):
        self.color_print.bold("Starting test....")
        test_data = {}
        for sensor in self.sensors:
            testdata = self.dataset.get_data(sensor)
            if testdata:
                for data in testdata:
                    if hasattr(data, '__len__'):
                        test_data[sensor] = True
                        self.color_print.ok_green(f'{sensor} ..........OK!')
                    else:
                        test_data[sensor] = False
                        self.color_print.fail(f'{sensor} ..........FAILED!')
            else:
                test_data[sensor] = False
                self.color_print.fail(f'{sensor} ..........FAILED!')

        if self.app_config.local_config.is_microphone:
            mic_test = self.mic.get_fft_data()
            if mic_test:
                test_data["microphone"] = True
                self.color_print.ok_green("Microphone ..........OK!")
            else:
                test_data["microphone"] = False
                self.color_print.fail("Microphone ..........FAILED!")

        return test_data
