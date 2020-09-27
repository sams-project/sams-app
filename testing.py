# from sensorlib.rgb import RGB
# import time
#
# led = RGB()
#
# led.green()
# time.sleep(3)
# led.blue()
# time.sleep(3)
# led.red()
# time.sleep(3)
# led.off()

from main.helper.error_helper import ErrorHelper

helper = ErrorHelper()

if helper.has_error("DS18B20"):
    print("its empty!")
else:
    print("hm!")
