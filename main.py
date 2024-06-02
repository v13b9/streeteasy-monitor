from requests import Session

from streeteasier.config import get_headers
from streeteasier.messager import send_messages
from streeteasier.scraper import scrape_search_results


def main():
    with Session() as s:
        s.headers.update(get_headers())
        new_listings = scrape_search_results(s)
        send_messages(new_listings, s)


if __name__ == '__main__':
    main()
