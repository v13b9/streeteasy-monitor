import re

from bs4 import BeautifulSoup

from .utility import build_url, get_datetime, get_area_map

# TODO: implement get validated neighborhood input

# TODO: convert input to list of codes based on area map

# TODO: implement get other parameter input - in flask?

area_map = get_area_map()

class Search:
    def __init__(self, monitor):
        self.session = monitor.session
        self.db = monitor.db
        self.kwargs = monitor.kwargs
        
        self.codes = [area_map[area] for area in self.kwargs['areas']]

        self.parameters = {
            # for full functionality, define handling for every possible search parameter and handle variable input
            'status': 'open',
            'price': f'{self.kwargs['min_price']}-{self.kwargs['max_price']}',
            'area': ','.join(self.codes),
            'beds': f'{self.kwargs['min_beds']}-{self.kwargs['max_beds']}',
        }

        print(f'self.parameters: {self.parameters}')

        self.url = build_url(**self.parameters)
        print(f'self.url: {self.url}')
        
        self.listings = []


    def fetch(self):
        r = self.session.get(self.url)
        parser = Parser(r.content, self.db)
        self.listings = parser.listings
        return self.listings


class Parser:
    def __init__(self, content, db):
        self.soup = BeautifulSoup(content, 'html.parser')
        self.existing_ids = db.get_existing_ids()

        self.filters = {
            'url': ['?featured=1', '?infeed=1'],
            'address': ['Herkimer', 'Fulton'],
            'neighborhood': [
                'Ocean Hill',
                'Flatbush',
                'Bushwick',
                'Weeksville',
                'Stuyvesant Heights',
            ]
        }

        self.price_pattern = re.compile(r'[$,]')

    def parse(self, card):
        listing_id = card.select_one('div.SRPCarousel-container')['data-listing-id']
        url = card.select_one('a.listingCard-globalLink')['href']
        price_text = card.select_one('span.price').text
        price = int(self.price_pattern.sub('', price_text))
        address = card.select_one('address.listingCard-addressLabel').text.strip()
        neighborhood_text = card.select_one('div.listingCardBottom--upperBlock p.listingCardLabel').text
        neighborhood = neighborhood_text.split(' in ')[-1].strip()

        return {
            'listing_id': listing_id,
            'url': url,
            'price': price,
            'address': address,
            'neighborhood': neighborhood,
        }

    def filter(self, target):
        if target['listing_id'] in self.existing_ids:
            return False

        for key, substrings in self.filters.items():
            target_value = target.get(key, '')
            if any(substring in target_value for substring in substrings):
                return False

        return True


    @property
    def listings(self):
        cards = self.soup.select('li.searchCardList--listItem')
        parsed = [self.parse(card) for card in cards]
        filtered = [card for card in parsed if self.filter(card)]
        
        if not filtered:
            print(f'{get_datetime()} No new listings\n')

        return filtered
