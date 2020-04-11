from main.dwh.token_handler import TokenHandler
from main.configuration.app_config import ApplicationConfig
from main.helper.microphone_helper import MicrophoneHelper
from main.dataset import Dataset
from main.helper.color import Color


class AppTest:
    def __init__(self):
        self.token_handler = TokenHandler()
        self.app_config = ApplicationConfig()
        self.mic = MicrophoneHelper()
        self.dataset = Dataset()
        self.color_print = Color()

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

    def dataset_test(self):
        sensors = ["DHT22", "DS18B20", "SCALE"]
        self.color_print.bold("Starting test....")
        for sensor in sensors:
            testdata = self.dataset.get_data(sensor)
            for data in testdata:
                if hasattr(data, '__len__'):
                    self.color_print.ok_green(f'{sensor} ..........OK!')
                else:
                    self.color_print.fail(f'{sensor} ..........FAILED!')

        mic_test = self.mic.get_fft_data()
        if mic_test:
            self.color_print.ok_green("Microphone ..........OK!")
        else:
            self.color_print.fail("Microphone ..........FAILED!")


testing = AppTest()
testing.dataset_test()
