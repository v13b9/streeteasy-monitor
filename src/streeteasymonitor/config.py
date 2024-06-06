from environs import Env
from fake_useragent import UserAgent

env = Env()
env.read_env()


def get_headers():
    ua = UserAgent()

    random_user_agent = ua.random
    default_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

    user_agent = random_user_agent or default_user_agent

    return {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://streeteasy.com/',
        'cache-control': 'no-cache',
        'Content-type': 'application/json',
        'origin': 'https://streeteasy.com',
    }


def get_field_values():
    return {
        'message': env('MESSAGE'),
        'phone': env('PHONE'),
        'search_partners': None,
        'email': env('EMAIL'),
        'name': env('NAME'),
    }


def setup_sqlalchemy(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env('DATABASE_URI')


def setup_supabase():
    from supabase import create_client

    supabase_url = env('SUPABASE_URL')
    supabase_key = env('SUPABASE_KEY')

    return create_client(supabase_url, supabase_key)
