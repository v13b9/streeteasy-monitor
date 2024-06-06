import requests

from src.streeteasymonitor.config import get_headers
from src.streeteasymonitor.messager import send_messages
from src.streeteasymonitor.scraper import scrape_search_results


def main():
    with requests.Session() as s:
        s.headers.update(get_headers())
        new_listings = scrape_search_results(s)
        send_messages(new_listings, s)


if __name__ == '__main__':
    main()
