import time
import sounddevice as sd
import scipy.io.wavfile
import datetime
from scipy import signal
import numpy as np
from numpy import median
from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS18B20
from main.configuration.local_config import LocalConfig
from main.configuration.user_config import UserConfig
from main.dwh.log_message import send_log
from main.helper.time_helper import get_time


class Dataset:
    def __init__(self):
        self.config = LocalConfig()
        self.user_credentials = UserConfig()
        self.config.get_config_data()
        try:
            self.dht22 = DHT22(int(self.config.dht22_pin))
        except Exception as e:
            send_log("Failed to initialize DHT22: {}".format(e), "error")

        try:
            self.scale = Scale()
        except Exception as e:
            send_log("Failed to initialize scale: {}".format(e), "error")

        try:
            self.DS18B20 = DS18B20()
        except Exception as e:
            send_log("Failed to initialize DS18B20: {}".format(e), "error")

        self.last_measured_weight = 0
        self.median_weight = 0

    def get_data(self, sensor_type):
        dataset = False
        if sensor_type == "DS18B20":
            dataset = self.get_ds18b20_data()
        elif sensor_type == "DHT22":
            dataset = self.get_dht22_data()
        elif sensor_type == "MICROPHONE":
            dataset = self.get_microphone_data()
        elif sensor_type == "SCALE":
            dataset = self.get_scale_data()

        return dataset

    def get_microphone_data(self):
        self.config.get_config_data()
        n_window = pow(2, 12)
        n_overlap = n_window / 2
        n_fft = n_window
        fs = int(self.config.audio_fs)

        try:
            audiodata = sd.rec(int(self.config.audio_duration) * fs, samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            [F, pxx] = scipy.signal.welch(data,
                                          fs=fs,
                                          window='hanning',
                                          nperseg=n_window,
                                          noverlap=n_overlap,
                                          nfft=n_fft,
                                          detrend=False,
                                          return_onesided=True,
                                          scaling='density'
                                          )
            temp_data = np.array(pxx).astype(float)
            data = temp_data.tolist()

            dataset = [[{
                "sourceId": "audio-{0}".format(self.user_credentials.client_id),
                "values": [
                    {
                        "ts": get_time(is_dataset=True),
                        "values": data[0]
                    },
                ]
            }]]
            if median(data[0]) == 0:  # no microphone available
                return False
            else:
                return dataset

        except Exception:
            return False

    def get_ds18b20_data(self):
        self.config.get_config_data()
        try:
            sensor_counter = self.DS18B20.device_count()
            dataset = []
            ds_temp = []
            if sensor_counter != 0 and sensor_counter != "NoneType":
                for x in range(sensor_counter):
                    for i in range(int(self.config.interval_median)):
                        value = self.DS18B20.tempC(x)
                        if value == 998 or value == 85.0:
                            send_log("DS18B20 does not work properly", "error")
                        else:
                            ds_temp.append(self.DS18B20.tempC(x))
                            time.sleep(3)

                    if range(len(ds_temp)) != 0 or ds_temp != "nan":
                        median_ds_temp = median(ds_temp)
                        dataset.append(
                            [{
                                "sourceId": "ds18b20-{0}-{1}".format(x, self.user_credentials.client_id),
                                "values": [
                                    {
                                        "ts": get_time(is_dataset=True),
                                        "value": float(median_ds_temp)
                                    },
                                ]
                            }]
                        )
                return dataset
            else:
                return False

        except Exception:
            return False

    def get_dht22_data(self):
        self.config.get_config_data()
        try:
            temp = []
            hum = []
            dataset = []
            for i in range(int(self.config.interval_median)):
                dhtdata = self.dht22.get_data()
                temp.append(dhtdata['temp'])
                hum.append(dhtdata['hum'])
                time.sleep(int(self.config.interval_wait_time_seconds))

            median_temp = median(temp)
            median_hum = median(hum)

            dataset.append(
                [{
                    "sourceId": "dht22-temperature-{0}".format(self.user_credentials.client_id),
                    "values": [
                        {
                            "ts": get_time(is_dataset=True),
                            "value": float(median_temp)
                        },
                    ]
                }]
            )
            dataset.append(
                [{
                    "sourceId": "dht22-humidity-{0}".format(self.user_credentials.client_id),
                    "values": [
                        {
                            "ts": get_time(is_dataset=True),
                            "value": float(median_hum)
                        },
                    ]
                }]
            )

            return dataset

        except Exception:
            return False

    def get_scale_data(self):
        self.config.get_config_data()
        weight = []
        control_measure = 0
        try:
            while control_measure < 2:
                control_measure += 1
                for i in range(int(self.config.interval_median)):
                    weight.append(self.scale.get_data())

                self.median_weight = median(weight)

                if self.last_measured_weight == self.median_weight:
                    control_measure += 1

            self.last_measured_weight = self.median_weight

            dataset = [[{
                "sourceId": "scale-{0}".format(self.user_credentials.client_id),
                "values": [
                    {
                        "ts": get_time(is_dataset=True),
                        "value": self.median_weight
                    }
                ]
            }]]

            return dataset

        except Exception:
            return False
