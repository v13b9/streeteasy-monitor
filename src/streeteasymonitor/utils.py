from datetime import datetime
from dateutil.tz import gettz

import json
import os

dir = os.path.dirname(os.path.abspath(__file__))


def get_datetime() -> str:
    """Get current timestamp for logging."""
    NYC = gettz('America/New_York')
    now = datetime.now().astimezone(NYC)
    date_now = now.strftime('%b %d, %Y')
    time_now = now.strftime('%I:%M %p')
    return f'[{date_now} - {time_now}]'


def get_area_map() -> dict[str, str]:
    """Load StreetEasy's area name and ID mapping."""
    with open(os.path.join(dir, 'data/areas.json'), 'r') as f:
        areas = json.load(f)
    return {area['name']: area['id'] for area in areas}


def build_url(**kwargs) -> str:
    """Construct search URL based on input parameters."""
    q = '|'.join([f'{k}:{v}' for k, v in kwargs.items()])
    return f'https://streeteasy.com/for-rent/nyc/{q}?sort_by=listed_desc'
