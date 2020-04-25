from main.helper.error_helper import ErrorHelper

errors = ErrorHelper()

sensor_errors = errors.get_sensor_with_error()

if errors.has_error("dht22"):
    print("yes")
else:
    print("no")
