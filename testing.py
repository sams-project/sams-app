from sensorlib.rgb import RGB
import time

led = RGB()

led.green()
time.sleep(3)
led.blue()
time.sleep(3)
led.red()
time.sleep(3)
led.off()
