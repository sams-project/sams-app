#  reset all credentials and prepare the system for production mode

import configparser
import shutil
import mapping
import os
from main.configuration.user_config import UserConfig
from main.configuration.token_config import TokenConfig
from main.helper.error_helper import ErrorHelper
from main.helper.color import Color

color = Color()


def reset_app_config():
    # delete application.ini
    # copy default.ini to application.ini
    try:
        os.remove(mapping.app_config)
        shutil.copyfile(mapping.default_config, mapping.app_config)
        color.ok_green("reset app config....done!")
    except Exception as e:
        color.fail(f'reset app config failed: {e}')


def reset_user_credentials():
    try:
        user_config = UserConfig()
        user_config.write_user_data("", "")
        color.ok_green("reset user credentials....done!")
    except Exception as e:
        color.fail(f'reset user credentials failed: {e}')


def reset_token_config():
    try:
        token_config = TokenConfig()
        token_config.reset_token()
        color.ok_green("reset token config....done!")
    except Exception as e:
        color.fail(f'reset token config failed : {e}')


def delete_log_files():
    try:
        shutil.rmtree(mapping.app_log)
        os.mkdir(mapping.app_log)
        color.ok_green("delete log files....done!")
    except Exception as e:
        color.fail(f'delete log files failed: {e}')


def reset_errors():
    try:
        errors = ErrorHelper()
        errors.reset_errors()
        color.ok_green("reset all errors....done!")
    except Exception as e:
        color.fail(f'reset all errors failed: {e}')


def write_version_number():
    print("\n")
    version = input("new version: ")
    version_file = open("/home/pi/sams_system/version.ini", "w+")
    version_file.write(str(version))
    version_file.close()
    color.ok_green(f"Version set to {version}")
    color.ok_green("DONE!")


reset_app_config()
reset_user_credentials()
reset_token_config()
reset_errors()
delete_log_files()
try:
    os.system("sudo rm /home/pi/update.py")
except Exception:
    pass
write_version_number()
