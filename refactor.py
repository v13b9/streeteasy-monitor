import json
import os
import re
import requests

from bs4 import BeautifulSoup

from src.streeteasymonitor.database import get_existing_ids
from src.streeteasymonitor.config import get_headers, get_field_values
from src.streeteasymonitor.utility import try_get

'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3000%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'

dir = os.path.dirname(os.path.abspath(__file__))

class Monitor:
    # running the function is essentially about:
        # opening a new session with new headers 
        # building the search url with parameters
        # GET search url
        # gather results
        # filter results
        # message results
    def __init__(self):
        print('__init__')
        self.session = requests.Session()
        self.session.headers.update(get_headers())

    def __enter__(self):
        print('__enter__')
        return self.session
    
    def __exit__(self, *args, **kwargs):
        print('__exit__')
        self.session.close()

    def __repr__(self):
        return f'< {self.session.headers} >'


    # class Search:

    # class Scrape:

    # class Message:

# load streeteasy code mapping to genereate area segment of search url based on input
def get_area_map():
    with open(os.path.join(dir, 'src/streeteasymonitor/data/areas.json'), 'r') as f:
        areas = json.load(f)
    return {area['id']: area['name'] for area in areas}

# TODO: implement get validated neighborhood input

# TODO: convert input to list of codes based on area map

codes = ['321', '364', '322', '325', '304', '320', '301', '319', '326', '329', '302', '310', '306', '307', '303', '412', '305', '109']

# TODO: implement get other parameter input - in flask?

# min_price_input = input('Min price? ')
# max_price_input = input('Max price? ')
# min_beds_input = input('Min number of beds? ')
# max_beds_input = input('Max number of beds? ')
min_price_input = 0
max_price_input = 3000
min_beds_input = 1
max_beds_input = 3


def build_url(**kwargs):
    q = '|'.join([f'{k}:{v}' for k, v in kwargs.items()])
    return f'https://streeteasy.com/for-rent/nyc/{q}?sort_by=listed_desc'

class Search:
    def __init__(self, session):
        self.price = f'{min_price_input}-{max_price_input}'
        self.area = ','.join([code for code in codes])
        self.beds = f'{min_beds_input}-{max_beds_input}'

        self.parameters = {
            # for full functionality, define handling for every possible search parameter and handle input
            'status': 'open',
            'price': self.price,
            'area': self.area,
            'beds': self.beds,
        }

        self.url = build_url(**self.parameters)
        self.session = session
        self.listings = []


    def fetch(self):
        self.r = self.session.get(self.url)
        parser = Parser(self.r.content)
        self.listings = parser.listings
        return self.listings
    

class Messager:
    def __init__(self, session):
        self.field_values = get_field_values()



class Parser:
    def __init__(self, content):
        self.soup = BeautifulSoup(content, 'html.parser')

        self.filters = {
            'url': ['?featured=1', '?infeed=1'],
            'address': ['Herkimer', 'Fulton'],
            'neighborhood': ['Ocean Hill', 'Flatbush', 'Bushwick', 'Weeksville', 'Stuyvesant Heights'],
            'listing_id': set(get_existing_ids()),
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
        filtered = [card for card in parsed if not self.filter(card)]

        if not filtered:
            print('No new listings')

        return filtered

def main():
    with Monitor() as monitor:
        search = Search(monitor)
        search.fetch()

if __name__ == '__main__':
    main()