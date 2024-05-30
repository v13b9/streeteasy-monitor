from fake_useragent import UserAgent

def get_headers():
    ua = UserAgent()

    random_user_agent = ua.random
    default_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

    user_agent = random_user_agent or default_user_agent

    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://streeteasy.com/',
        'cache-control': 'no-cache',
        'Content-type': 'application/json',
        'origin': 'https://streeteasy.com',
    }

    return headers