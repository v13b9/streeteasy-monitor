import re

from bs4 import BeautifulSoup

from database import get_existing_ids
from utility import try_get

test_search_url = 'https://streeteasy.com/for-rent/new-jersey?sort_by=price_asc'
search_url = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'

existing_ids = get_existing_ids()


def scrape_search_results(s):
    r = try_get(test_search_url, 'scrape_search_results', s)
    soup = BeautifulSoup(r.content, 'html.parser')
    cards = soup.select('li.searchCardList--listItem')

    return get_new_listings(cards)


def get_new_listings(cards):
    new_listings = []

    for card in cards:
        listing_id = int(
            card.select_one('div.SRPCarousel-container')['data-listing-id']
        )
        if listing_id not in existing_ids:
            url = card.select_one('a.listingCard-globalLink')['href']
            price = int(re.sub(r'[$,]', '', card.select_one('span.price').text))
            address = card.select_one('address.listingCard-addressLabel').text.strip()
            neighborhood = (
                card.select_one('div.listingCardBottom--upperBlock p.listingCardLabel')
                .text.split(' in ')[-1]
                .strip()
            )

            new_listing = {
                'listing_id': listing_id,
                'url': url,
                'price': price,
                'address': address,
                'neighborhood': neighborhood,
            }

            print(f'listing_id: {listing_id}')
            # print(f'url: {url}')
            # print(f'price: {price}')
            # print(f'address: {address}')
            # print(f'neighborhood: {neighborhood}')
            new_listings.append(new_listing)

    return new_listings
