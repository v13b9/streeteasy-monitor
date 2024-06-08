import re

from bs4 import BeautifulSoup

from .utility import build_url

test_search_url = (
    'https://streeteasy.com/for-rent/new-jersey/price:-2000?sort_by=listed_desc'
)

search_url_broad = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3000%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'
search_url_narrow = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-2900%7Carea:310,306,305,321,364,322,307,303,304,320,301,319,326,302%7Cbeds:1-3?sort_by=listed_desc'

# TODO: implement get validated neighborhood input

# TODO: convert input to list of codes based on area map

# TODO: implement get other parameter input - in flask?

min_price = 0
max_price = 3000
min_beds = 1
max_beds = 3

codes = [
    '321',
    '364',
    '322',
    '325',
    '304',
    '320',
    '301',
    '319',
    '326',
    '329',
    '302',
    '310',
    '306',
    '307',
    '303',
    '412',
    '305',
    '109',
]


class Search:
    def __init__(self, monitor):
        self.price = f'{min_price}-{max_price}'
        self.area = ','.join([code for code in codes])
        self.beds = f'{min_beds}-{max_beds}'

        self.parameters = {
            # for full functionality, define handling for every possible search parameter and handle variable input
            'status': 'open',
            'price': self.price,
            'area': self.area,
            'beds': self.beds,
        }

        # self.url = build_url(**self.parameters)
        self.url = search_url_narrow
        self.session = monitor.session
        self.db = monitor.db
        self.listings = []

    def fetch(self):
        r = self.session.get(self.url)
        parser = Parser(r.content, self.db)
        self.listings = parser.listings
        return self.listings


class Parser:
    def __init__(self, content, db):
        self.soup = BeautifulSoup(content, 'html.parser')

        self.filters = {
            'url': ['?featured=1', '?infeed=1'],
            'address': ['Herkimer', 'Fulton'],
            'neighborhood': [
                'Ocean Hill',
                'Flatbush',
                'Bushwick',
                'Weeksville',
                'Stuyvesant Heights',
            ],
            'listing_id': db.get_existing_ids(),
        }

    def parse(self, card):
        return {
            'listing_id': card.select_one('div.SRPCarousel-container')['data-listing-id'],
            'url': card.select_one('a.listingCard-globalLink')['href'],
            'price': int(re.sub(r'[$,]', '', card.select_one('span.price').text)),
            'address': card.select_one('address.listingCard-addressLabel').text.strip(),
            'neighborhood': (
                card.select_one('div.listingCardBottom--upperBlock p.listingCardLabel')
                .text.split(' in ')[-1]
                .strip()
            ),
        }

    def filter(self, target):
        for key, substrings in self.filters.items():
            target_value = target.get(key, '')
            if any(substring in target_value for substring in substrings):
                return True
        return False

    @property
    def listings(self):
        cards = self.soup.select('li.searchCardList--listItem')
        parsed = [self.parse(card) for card in cards]
        # print(f'parsed: {parsed}')
        filtered = [card for card in parsed if not self.filter(card)]
        # print(f'filtered: {filtered}')

        if not filtered:
            print('No new listings')

        return filtered
