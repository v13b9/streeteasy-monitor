from datetime import datetime
from dateutil.tz import gettz
import random
import re
import requests
import time

from bs4 import BeautifulSoup

from headers import get_headers
from env_config import get_field_values, setup_supabase

supabase = setup_supabase()
# scrapeops_key = env('SCRAPEOPS_KEY')

field_values = get_field_values()

test_search_url = 'https://streeteasy.com/for-rent/nyc?sort_by=sqft_desc'
search_url = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'

listings_data = supabase.table('listings').select('*').execute().data
existing_ids = [listing['listing_id'] for listing in listings_data]

api_url = 'https://api-v6.streeteasy.com/'

start_query = """
    fragment Children on KoiosElement {
    children {
        ...ChildrenFields
        children {
        ...ChildrenFields
        children {
            ...ChildrenFields
            children {
            ...ChildrenFields
            children {
                ...ChildrenFields
                children {
                ...ChildrenFields
                children {
                    ...ChildrenFields
                    children {
                    ...ChildrenFields
                    children {
                        ...ChildrenFields
                        children {
                        ...ChildrenFields
                        }
                    }
                    }
                }
                }
            }
            }
        }
        }
    }
    }
    fragment ChildrenFields on KoiosElement {
    type
    componentType
    config
    field {
        name
        type
        value
        error
    }
    }

    mutation StartPageFlow($request: KoiosStartPageflowRequest!) {
    data: startPageflow(request: $request) {
        ... on KoiosErrorResponse {
        code
        message
        errorFields
        }

        ... on KoiosStartPageflowSuccess {
        code
        pageflowId
        pageflowType

        page {
            id
            config
            elements {
            type
            componentType
            config
            field {
                name
                type
                value
                error
            }
            ...Children
            }
        }

        pageNum
        totalPages
        containerType
        config
        replyToken
        }
    }
    }
"""

start_variables = {
    'request': {
        'name': 'ContactBox-Rentals-Consumer-AskQuestion-v0.0.2',
        'context': {
            '_client': {
                'koiosClient': 'koios.js v0.0.5',
                # "deviceId": deviceId,
            },
            # "rental_id": listing['listing_id'],
        },
        # "fieldValues": {
        #     "name": "",
        #     "phone": "",
        #     "email": ""
        # },
        'isStrict': False,
    }
}

finish_query = """
    mutation FinishPageflow($request: KoiosFinishPageflowRequest) {
        data: finishPageflow(request: $request) {
            ... on KoiosErrorResponse {
                code
                message
                errorFields
            }

            ... on KoiosFinishPageflowSuccess {
                code
                returnConfig
            }
        }
    }
"""


def wait():
    time.sleep(random.randint(0, 3))


def get_datetime():
    tz = gettz()
    now = datetime.now(tz)
    time_now = now.strftime('%l:%M %p')
    date_now = now.strftime('%B %e, %Y')
    return date_now, time_now


def try_post(url, json_data, func_name):
    date_now, time_now = get_datetime()
    print(f'\n[{date_now} {time_now}] Trying POST {url} - {func_name}...')
    wait()
    r = s.post(url, json=json_data)
    print(f'Status code: {r.status_code} {r.reason}')
    return r


def try_get(url, func_name):
    date_now, time_now = get_datetime()
    print(f'[{date_now} {time_now}] Trying GET {url} - {func_name}...')
    wait()
    r = s.get(url)
    print(f'Status code: {r.status_code} {r.reason}')
    return r


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


def scrape_search_results(url: str):
    r = try_get(url, 'scrape_search_results')
    soup = BeautifulSoup(r.content, 'html.parser')
    cards = soup.select('li.searchCardList--listItem')

    return get_new_listings(cards)


def send_messages(listings):
    for listing_id in [listing['listing_id'] for listing in listings]:
        pageflow_id, reply_token = get_pageflow_id(listing_id)
        submit_message(pageflow_id, reply_token)


def get_pageflow_id(listing_id):
    start_variables['request']['context']['rental_id'] = listing_id

    start_json_data = {
        'query': start_query,
        'variables': start_variables,
    }

    r = try_post(api_url, start_json_data, 'get_pageflow_id')

    pageflow_id = r.json()['data']['data']['pageflowId']
    reply_token = r.json()['data']['data']['replyToken']

    print('pageflowId:', pageflow_id)
    print('replyToken:', reply_token)

    return pageflow_id, reply_token


def submit_message(pageflow_id, reply_token):
    finish_variables = {
        'request': {
            'pageflowId': pageflow_id,
            'replyToken': reply_token,
            'fieldValues': field_values,
        }
    }

    finish_json_data = {
        'query': finish_query,
        'variables': finish_variables,
    }

    try_post(api_url, finish_json_data, 'submit_message')


def main(s):
    s.headers.update(get_headers())
    new_listings = scrape_search_results(test_search_url)
    send_messages(new_listings)
    supabase.table('listings').insert(new_listings).execute()


if __name__ == '__main__':
    with requests.Session() as s:
        main(s)
