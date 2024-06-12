from environs import Env
from fake_useragent import UserAgent


class Config:
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

    # def setup_sqlalchemy(self, app):
    #     app.config['SQLALCHEMY_DATABASE_URI'] = self.env('DATABASE_URI')

    def setup_supabase(self):
        from supabase import create_client

        supabase_url = self.env('SUPABASE_URL')
        supabase_key = self.env('SUPABASE_KEY')

        return create_client(supabase_url, supabase_key)
