import datetime
import os
import pytz


def get_time(is_dataset=False):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if not is_dataset:
        return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0]
    else:
        return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0] + 'Z'


def get_diff_seconds(last_time):
    now = get_time()
    if last_time != "":
        diff = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S') \
                - datetime.datetime.strptime(last_time, '%Y-%m-%dT%H:%M:%S')
        return int(diff.seconds)
    else:
        return False


def set_timezone(timezone):
    try:
        new_timezone = 'sudo timedatectl set-timezone {}'.format(timezone)
        os.system(new_timezone)
    except Exception as e:
        print(e)
