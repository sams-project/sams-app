from gpiozero import RGBLED


class RGB:
    def __init__(self):
        self.led = RGBLED(red=10, green=9, blue=11)

    def green(self):
        self.led.color = (0, 1, 0)

    def red(self):
        self.led.color = (1, 0, 0)

    def blue(self):
        self.led.color = (0, 0, 1)

    def off(self):
        self.led.color = (0, 0, 0)
