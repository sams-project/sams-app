import Adafruit_DHT
from main.dwh.log_message import send_log


class DHT22:
    def __init__(self, pin):
        self.pin = pin
        self.data = {}

    def get_data(self):
        try:
            sensor = Adafruit_DHT.DHT22
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
            self.data = {"temp": round(float(temperature), 2), "hum": round(float(humidity), 2)}

            return self.data

        except Exception as e:
            send_log(f'DHT22 sensor connected? : {e}', "warning")
