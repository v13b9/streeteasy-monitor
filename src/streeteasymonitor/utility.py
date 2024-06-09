from datetime import datetime
from dateutil.tz import gettz
import random
import json
import os
import time

dir = os.path.dirname(os.path.abspath(__file__))


def wait():
    time.sleep(random.randint(0, 3))


def get_datetime():
    NYC = gettz('America/New_York')
    now = datetime.now().astimezone(NYC)
    date_now = now.strftime('%b %d, %Y')
    time_now = now.strftime('%I:%M %p')
    return f'[{date_now} - {time_now}]'


def try_get(url, func_name, s):
    date_now, time_now = get_datetime()
    print(f'[{date_now} {time_now}] Trying GET {url} - {func_name}...')
    # wait()
    r = s.get(url)
    print(f'Status code: {r.status_code} {r.reason}')
    return r


def try_post(url, json_data, func_name, s):
    date_now, time_now = get_datetime()
    print(f'\n[{date_now} {time_now}] Trying POST {url} - {func_name}...')
    # wait()
    r = s.post(url, json=json_data)
    print(f'Status code: {r.status_code} {r.reason}')
    return r


# load streeteasy code mapping to genereate area segment of search url based on input
def get_area_map():
    with open(os.path.join(dir, 'src/streeteasymonitor/data/areas.json'), 'r') as f:
        areas = json.load(f)
    return {area['id']: area['name'] for area in areas}


def build_url(**kwargs):
    # TODO: flesh out url construction for all possible parameters and sorting methods
    q = '|'.join([f'{k}:{v}' for k, v in kwargs.items()])
    return f'https://streeteasy.com/for-rent/nyc/{q}?sort_by=listed_desc'
