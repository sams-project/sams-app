import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Device:
    def __init__(self, pin, device_type):
        self.pin = pin
        self.type = device_type

    def on(self):
        GPIO.setup(self.pin, GPIO.OUT)
        if self.type == "led":
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        GPIO.setup(self.pin, GPIO.OUT)
        if self.type == "led":
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)
