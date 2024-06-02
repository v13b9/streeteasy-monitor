from requests import Session

from src.streeteasier.config import get_headers
from src.streeteasier.messager import send_messages
from src.streeteasier.scraper import scrape_search_results


def main():
    with Session() as s:
        s.headers.update(get_headers())
        new_listings = scrape_search_results(s)
        send_messages(new_listings, s)


if __name__ == '__main__':
    main()
