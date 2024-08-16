from environs import Env
from fake_useragent import UserAgent


class Config:
    defaults = {
        'min_price': 3000,
        'max_price': 3100,
        'min_beds': 1,
        'max_beds': 3,
        'baths': 1,
        'areas': [
            'Carroll Gardens',
            'Clinton Hill',
            'Cobble Hill',
            # 'Crown Heights',
            'Fort Greene',
            'Gowanus',
            'Greenpoint',
            'Park Slope',
            'Prospect Heights',
            # 'Prospect Lefferts Gardens',
            'Williamsburg',
            'Bedford-Stuyvesant',
            'Boerum Hill',
            'DUMBO',
            'Downtown Brooklyn',
            # 'Ridgewood',
            'Brooklyn Heights',
            # 'Lower East Side',
            'Upper East Side',
        ],
        'amenities': [
            'pets',
            'doorman',
            # 'laundry',
            # 'elevator',
            # 'private_outdoor_space',
            # 'dishwasher',
            # 'washer_dryer',
            # 'gym',
        ],
        'no_fee': False,
    }

    filters = {
        'url': [
            '?featured=1',
            '?infeed=1',
        ],
        'address': [
            'Herkimer',
            'Fulton',
        ],
        'neighborhood': [
            'Ocean Hill',
            'Flatbush',
            'Bushwick',
            'Weeksville',
            'Stuyvesant Heights',
            'New Development',
        ],
    }

    def __init__(self):
        self.env = Env()
        self.env.read_env()

    def get_headers(self):
        self.ua = UserAgent()
        self.random_user_agent = self.ua.random
        self.default_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        self.user_agent = self.random_user_agent or self.default_user_agent

        return {
            'user-agent': self.user_agent,
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://streeteasy.com/',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://streeteasy.com',
        }

    def get_field_values(self):
        return {
            'message': self.env('MESSAGE', default=''),
            'phone': self.env('PHONE', default=''),
            'email': self.env('EMAIL', default=''),
            'name': self.env('NAME', default=''),
            'search_partners': None,
        }
