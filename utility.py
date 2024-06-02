from datetime import datetime
from dateutil.tz import gettz
import random
import time


def wait():
    time.sleep(random.randint(0, 3))


def get_datetime():
    tz = gettz()
    now = datetime.now(tz)
    time_now = now.strftime('%l:%M %p')
    date_now = now.strftime('%B %e, %Y')
    return date_now, time_now


def try_get(url, func_name, s):
    date_now, time_now = get_datetime()
    print(f'[{date_now} {time_now}] Trying GET {url} - {func_name}...')
    wait()
    r = s.get(url)
    print(f'Status code: {r.status_code} {r.reason}')
    return r


def try_post(url, json_data, func_name, s):
    date_now, time_now = get_datetime()
    print(f'\n[{date_now} {time_now}] Trying POST {url} - {func_name}...')
    wait()
    r = s.post(url, json=json_data)
    print(f'Status code: {r.status_code} {r.reason}')
    return r
