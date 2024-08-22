import json
import re

from bs4 import BeautifulSoup

from .config import Config
from .utils import build_url, get_datetime, get_area_map


class Search:
    """A search based on the current session, database instance, and keyword arguments for constructing a StreetEasy search URL.

    Attributes:
        area_map (dict[str, str]): A mapping of StreetEasy's neighborhood names and corresponding codes used for URL construction.
    """

    area_map: dict[str, str] = get_area_map()

    def __init__(self, monitor) -> None:
        """Initializes the search.

        Args:
            monitor (Monitor): A Monitor instance encapsulating a session, a database connection, and keyword arguments for constructing a search URL.

        Attributes:
            session (requests.Session): The session instance.
            db (Database): The database instance.
            kwargs (dict[str, str]): The search parameter components.
            codes (list[str, str]): The StreetEasy neighborhood codes corresponding to selected neighborhood names.

            price (str): The price range component of the search URL.
            area (str): The neighborhood code component of the search URL.
            beds (str): The number of beds component of the search URL.

            parameters (dict[str, str]): Dictionary mapping query components for URL construction.
            url (str): Search URL for the current query.
            listings (list[dict[str, str]]): Listings corresponding to the current search - initially empty.
        """

        self.session = monitor.session
        self.db = monitor.db
        self.kwargs = monitor.kwargs

        self.codes = [Search.area_map[area] for area in self.kwargs['areas']]

        self.area = ','.join(self.codes)
        self.price = f"{self.kwargs['min_price']}-{self.kwargs['max_price']}"
        self.beds = f"{self.kwargs['min_beds']}-{self.kwargs['max_beds']}"
        self.baths = f">={self.kwargs['baths']}"
        self.amenities = f"{','.join(self.kwargs['amenities'])}"
        self.no_fee = f"{1 if self.kwargs['no_fee'] == True else ''}"


        self.parameters = {
            'status': 'open',
            'price': self.price,
            'area': self.area,
            'beds': self.beds,
            'baths': self.baths,
            'amenities': self.amenities,
            'no_fee': self.no_fee,
        }

        self.url = build_url(**self.parameters)
        self.listings = []

    def fetch(self) -> list[dict[str, str]]:
        """Check the search URL for new listings."""
        print(f'Running script with parameters:\n{json.dumps(self.parameters, indent=2)}\n')
        print(f'URL: {self.url}')
        self.r = self.session.get(self.url)
        if self.r.status_code == 200:
            parser = Parser(self.r.content, self.db)
            self.listings = parser.listings

        if not self.listings:
            print(f'{get_datetime()} No new listings.\n')

        return self.listings


class Parser:
    """Separates parsing functionality from search.

    Attributes:
        price_pattern (re.Pattern): Regular expression used for stripping commas and dollar signs from listing price.
    """

    price_pattern = re.compile(r'[$,]')

    def __init__(self, content: bytes, db) -> None:
        """Initialize the parse object.

        Args:
            content (bytes): HTML content of a successful GET request to the search URL.
            db (Database): Database instance used for fetching listing IDs that already exist in the database.

        Attributes:
            soup (bs4.BeautifulSoup): Beautiful Soup object for parsing HTML contents.
            existing_ids (list[str]): Listing IDs that have already been stored in the database.
        """

        self.soup = BeautifulSoup(content, 'html.parser')
        self.existing_ids = db.get_existing_ids()

    def parse(self, card) -> dict[str, str]:
        """Parse the contents of one listing."""
        listing_id = card.select_one('div.SRPCarousel-container')['data-listing-id']
        url = card.select_one('a.listingCard-globalLink')['href']
        price = Parser.price_pattern.sub('', card.select_one('span.price').text)
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

    def filter(self, target) -> bool:
        """Filter a listing based on attributes not captured by StreetEasy's interface natively."""
        if target['listing_id'] in self.existing_ids:
            return False

        for key, substrings in Config.filters.items():
            target_value = target.get(key, '')
            if any(substring in target_value for substring in substrings):
                return False

        return True

    @property
    def listings(self) -> dict[str, str]:
        """Return all parsed and filtered listings."""
        cards = self.soup.select('li.searchCardList--listItem')
        parsed = [self.parse(card) for card in cards]
        filtered = [card for card in parsed if self.filter(card)]
        return filtered
