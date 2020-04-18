import RPi.GPIO as GPIO
from numpy import median
import time
from sensorlib.hx711 import HX711
from main.configuration.local_config import LocalConfig
from main.dwh.log_message import send_log
GPIO.setmode(GPIO.BCM)


class Scale:
    def __init__(self):
        self.config = LocalConfig()  # config init
        self.hx = HX711(5, 6)  # initialize scale
        self.ratio = 0  # scale ratio for calibration
        self.offset = 0
        self.value = 0
        self.result = 0
        self.data = 0
        if self.config.scale_calibrated:
            self.hx.set_offset(float(self.config.scale_offset))
            self.hx.set_scale(float(self.config.scale_ratio))

    def setup(self):
        try:
            self.offset = self.hx.read_average()
            self.hx.set_offset(self.offset)
            return True
        except Exception:
            return False

    def has_error(self):
        value_list = []
        try:
            for x in range(15):
                self.hx.power_up()
                value_list.append(self.hx.get_grams())
                self.hx.power_down()
                time.sleep(0.1)

            median_val = median(value_list)
            if value_list[3] == median_val:
                return True
            else:
                return False

        except Exception:
            return True

    def calibrate(self, weight):
        try:
            self.value = int(weight)

            median_weight_list = []
            median_offset_list = []

            for x in range(7):
                median_weight_list.append(self.hx.read_average())

            for x in range(7):
                median_offset_list.append(self.hx.get_offset())

            average_weight = median(median_weight_list)
            average_offset = median(median_offset_list)

            measured_weight = (average_weight - average_offset)
            self.ratio = int(measured_weight) / self.value
            self.hx.set_scale(self.ratio)
            self.config.set_config_data("SCALE", "ratio", self.ratio)
            self.config.set_config_data("SCALE", "offset", self.hx.get_offset())
            self.config.set_config_data("SCALE", "calibrated", 1)
            self.config.set_config_data("DEFAULT", "start", 1)
            return True
        except ValueError:
            return False

    def get_data(self):
        try:
            self.hx.power_up()
            val = self.hx.get_grams()
            measure_weight = round((val / 1000), 2)
            self.hx.power_down()
            return measure_weight
        except Exception as e:
            send_log(f'Cannot get Scale data: {e}', "error")

    def reset(self):
        self.config.set_config_data("SCALE", "ratio", 0)
        self.config.set_config_data("SCALE", "offset", 0)
        self.config.set_config_data("SCALE", "calibrated", 0)

    def tare(self):
        self.hx.tare()
        self.config.set_config_data("SCALE", "offset", self.hx.get_offset())

    @staticmethod
    def clean():
        GPIO.cleanup()
