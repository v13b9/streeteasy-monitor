from environs import Env
from fake_useragent import UserAgent


class Config:
    default = {
        'min_price': 0,
        'max_price': 2900,
        'min_beds': 1,
        'max_beds': 3,
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
    }

    filters = {
        'url': ['?featured=1', '?infeed=1'],
        'address': ['Herkimer', 'Fulton'],
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
            'message': self.env('MESSAGE'),
            'phone': self.env('PHONE'),
            'search_partners': None,
            'email': self.env('EMAIL'),
            'name': self.env('NAME'),
        }

    def setup_supabase(self):
        from supabase import create_client

        supabase_url = self.env('SUPABASE_URL')
        supabase_key = self.env('SUPABASE_KEY')

        return create_client(supabase_url, supabase_key)
