import re

from bs4 import BeautifulSoup

from .database import get_existing_ids
from .utility import try_get

test_search_url = 'https://streeteasy.com/for-rent/new-jersey/price:-2000?sort_by=listed_desc'
search_url = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'

filters = {
    'listing_id': get_existing_ids(),
    'url': ['?featured=1', '?infeed=1'],
    'address': ['Herkimer'],
    'neighborhood': ['Ocean Hill', 'Flatbush', 'Bushwick'],
}


def matches_filters(target):
    for key, substrings in filters.items():
        target_value = target.get(key, "")
        if any(substring in target_value for substring in substrings):
            return True
    return False


def scrape_search_results(s):
    r = try_get(test_search_url, 'scrape_search_results', s)
    soup = BeautifulSoup(r.content, 'html.parser')
    cards = soup.select('li.searchCardList--listItem')

    return get_new_listings(cards)


def get_listing_info(card):
    listing_id = card.select_one('div.SRPCarousel-container')['data-listing-id']
    url = card.select_one('a.listingCard-globalLink')['href']
    price = int(re.sub(r'[$,]', '', card.select_one('span.price').text))
    address = card.select_one('address.listingCard-addressLabel').text.strip()
    neighborhood = (
        card.select_one('div.listingCardBottom--upperBlock p.listingCardLabel')
        .text.split(' in ')[-1]
        .strip()
    )

    return {
        'listing_id': listing_id,
        'url': url,
        'price': price,
        'address': address,
        'neighborhood': neighborhood,
    }


def get_new_listings(cards):
    new_listings = [
        new_listing
        for card in cards
        if not matches_filters(
            new_listing := get_listing_info(card))
            and not print(f'Listing added: {new_listing["url"]}')
    ]

    if not new_listings:
        print('No new listings\n')

    return new_listings
