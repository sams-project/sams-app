from flask import Flask, render_template, request
from main.configuration.user_config import UserConfig
from main.configuration.app_config import ApplicationConfig
from sensorlib.scale import Scale
from main.helper.wifi_helper import WifiHelper
from main.helper.test_helper import AppTest
from main.helper.time_helper import set_timezone
from main.helper.error_helper import ErrorHelper
import os
import time

app = Flask(__name__)
user_config = UserConfig()
app_config = ApplicationConfig()
scale = Scale()
wifi = WifiHelper()
testing = AppTest()
error_helper = ErrorHelper()


@app.route('/')
def start():
    user = user_config.get_user_data()
    app_config.local_config.get_config_data()
    is_start = app_config.local_config.start
    is_scale = app_config.local_config.is_scale
    return render_template("start.html",
                           title="start",
                           user_data=user,
                           calibrated=app_config.local_config.scale_calibrated,
                           is_start=is_start,
                           is_scale=is_scale
                           )


@app.route('/', methods=['POST'])
def set_user():
    user_id = request.form.get("user")
    user_secret = request.form.get("secret")
    user_config.write_user_data(user_id, user_secret)
    user = user_config.get_user_data()
    is_start = app_config.local_config.start
    is_scale = app_config.local_config.is_scale

    return render_template('start.html',
                           title="start",
                           calibrated=app_config.local_config.scale_calibrated,
                           user_data=user,
                           is_start=is_start,
                           is_scale=is_scale
                           )


# ####################### SCALE SETUP ######################################
@app.route('/calibrate')  # start calibrate the scale
def calibrate():
    scale.setup()
    return render_template('calibrate.html', title="calibrate")


@app.route('/calibrate_offset')  # calibrate the offset starting
def calibrate_offset():
    return render_template('calibrate_offset.html', title="calibrate offset")


@app.route('/calibrate_offset', methods=['POST'])  # send known weight to calibrate
def config_scale():
    calibrated = False
    if scale.calibrate(request.form['weight']):
        if app_config.local_config.get_config_data():
            calibrated = app_config.local_config.scale_calibrated
    return render_template('calibrated.html', title="calibrated", calibrated=calibrated)


@app.route('/reset')  # write that the app is ready to start and reboot system
def start_and_reset():
    app_config.local_config.set_config_data("DEFAULT", "start", 1)
    time.sleep(5)
    os.system('sudo reboot')
    return "Reset and Start..."


@app.route('/reset', methods=['POST'])  # reboot system
def reset():
    os.system('sudo reboot')
    return "Restart..."


# ####################### END SCALE SETUP ######################################


@app.route('/settings')  # setting page
def settings():
    user_data = user_config.get_user_data()
    conf = get_config_data()
    signal = wifi.get_signal_strength()
    gigabytes_avail = testing.get_available_space()
    return render_template('settings.html', title="setting",
                           wifi_signal=signal,
                           avail_space=gigabytes_avail,
                           user_data=user_data,
                           config=conf)


@app.route('/settings', methods=['POST'])
def setting():
    try:
        if request.form.get("reset") == "":
            scale.reset()
        if request.form.get("tare") == "":
            scale.tare()
        if request.form.get("reset_error") == "":
            error_helper.reset_errors()
        if request.form.get("user_reset") == "":
            user_config.write_user_data("", "")

    except Exception as error:
        print(error)

    user_data = user_config.get_user_data()
    conf = get_config_data()
    signal = wifi.get_signal_strength()
    gigabytes_avail = testing.get_available_space()
    return render_template('settings.html', title="setting",
                           config=conf,
                           wifi_signal=signal,
                           avail_space=gigabytes_avail,
                           user_data=user_data)


@app.route('/timezone', methods=['POST'])
def timezone():
    app_config.local_config.get_config_data()
    new_timezone = app_config.local_config.timezone
    if request.form.get("timezone"):
        new_timezone = request.form.get("timezone")
        set_timezone(str(new_timezone))
        app_config.local_config.set_config_data("DEFAULT", "timezone", new_timezone)

    return render_template("timezone.html", timezone=new_timezone)


def get_config_data():
    if wifi.is_online():
        app_config.sync_config()
    else:
        app_config.local_config.get_config_data()

    conf = app_config.local_config
    return conf


if __name__ == '__main__':
    app.run(host='0.0.0.0')
