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
    now = get_token_time()
    if last_time != "":
        diff = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S') \
               - datetime.datetime.strptime(last_time, '%Y-%m-%dT%H:%M:%S')
        return float(diff.total_seconds())
    else:
        return False


def get_token_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0]


def set_timezone(timezone):
    try:
        new_timezone = 'sudo timedatectl set-timezone {}'.format(timezone)
        os.system(new_timezone)
    except Exception as e:
        print(e)
