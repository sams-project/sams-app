import datetime
from datetime import timedelta


def get_time(is_dataset=False):
    now = datetime.datetime.now()
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
