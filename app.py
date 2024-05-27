import random
import re
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

random_user_agent = ua.random
default_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

user_agent = random_user_agent or default_user_agent

headers = {
    'User-Agent': user_agent,
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://streeteasy.com/',
    'cache-control': 'no-cache',
    'Content-type':'application/json',
    'origin': 'https://streeteasy.com',
}

test_search_url = 'https://streeteasy.com/for-rent/nyc?sort_by=sqft_desc'
search_url = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3?sort_by=listed_desc'    

with requests.Session() as s:

    s.headers.update(headers)

    # r = s.get(
    #     url='https://proxy.scrapeops.io/v1/',
    #     params={
    #         'api_key': 'ff34d53e-11ae-48d1-8700-80a764a42210',
    #         'url': search_url, 
    #     },
    # )

    # scrape search results
    print(f'Trying GET {test_search_url}...')
    time.sleep(random.randint(0, 3))
    r = s.get(test_search_url)
    print(f'Status code: {r.status_code} {r.reason}')

    soup = BeautifulSoup(r.content, 'html.parser')
    cards = soup('li', class_='searchCardList--listItem')

    listings = []

    for card in cards:
        listing_id = card.find('div', class_='SRPCarousel-container')['data-listing-id']
        url = card.find('a', class_='listingCard-globalLink')['href']
        price = int(re.sub(r'[$,]', '', card.find('span', class_='price').text))
        address = card.find('address', class_='listingCard-addressLabel').text.strip()
        neighborhood = re.sub('Rental Unit in', '', card.find('p', class_='listingCardLabel').text).strip()

        listing = {
            'listing_id': listing_id,
            'url': url,
            'price': price,
            'address': address,
            'neighborhood': neighborhood,
        }

        print('address:', address)

        listings.append(listing)
    
    # send message
    for url in [listing['url'] for listing in listings]:

        print(f'\nTrying GET {url}...')
        time.sleep(random.randint(0, 3))
        r = s.get(url)
        print(f'Status code: {r.status_code} {r.reason}')

        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup('script')[-2].string
        pattern = r'(?<=deviceId\:\s\")[a-zA-Z0-9-]*(?=\",)'
        deviceId = re.search(pattern, script).group()

        print('deviceId:', deviceId)

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
            "request": {
                "name": "ContactBox-Rentals-Consumer-AskQuestion-v0.0.2",
                "context": {
                "_client": {
                    "koiosClient": "koios.js v0.0.5",
                    "deviceId": deviceId,
                },
                "rental_id": 4397849,
                },
                "fieldValues": {
                    "name": "",
                    "phone": "",
                    "email": ""
                },
                "isStrict": False
            }
        }

        start_json_data = {
            "query": start_query,
            "variables": start_variables,
        }

        print(f'\nTrying POST {api_url}...')
        time.sleep(random.randint(0, 3))
        r = s.post(api_url, json=start_json_data, headers=headers)
        print(f'Status code: {r.status_code} {r.reason}')
        # print('JSON:', r.json())

        pageflowId = r.json()['data']['data']['pageflowId']
        replyToken = r.json()['data']['data']['replyToken']

        print('pageflowId:', pageflowId)
        print('replyToken:', replyToken)


        

    # test_url = 'https://streeteasy.com/building/129-franklin-street-jersey_city/a5'
    
    # print(f'Trying GET {test_url}...')
    # time.sleep(random.randint(0, 3))
    # r = s.get(test_url)
    # print('Status code:', r.status_code, r.reason)

    # soup = BeautifulSoup(r.content, 'html.parser')
    # script = soup('script')[-2].string
    # pattern = r'(?<=deviceId\:\s\")[a-zA-Z0-9-]*(?=\",)'
    # deviceId = re.search(pattern, script).group()
    
    # api_url = 'https://api-v6.streeteasy.com/'

    # start_query = """
    #     fragment Children on KoiosElement {
    #     children {
    #         ...ChildrenFields
    #         children {
    #         ...ChildrenFields
    #         children {
    #             ...ChildrenFields
    #             children {
    #             ...ChildrenFields
    #             children {
    #                 ...ChildrenFields
    #                 children {
    #                 ...ChildrenFields
    #                 children {
    #                     ...ChildrenFields
    #                     children {
    #                     ...ChildrenFields
    #                     children {
    #                         ...ChildrenFields
    #                         children {
    #                         ...ChildrenFields
    #                         }
    #                     }
    #                     }
    #                 }
    #                 }
    #             }
    #             }
    #         }
    #         }
    #     }
    #     }
    #     fragment ChildrenFields on KoiosElement {
    #     type
    #     componentType
    #     config
    #     field {
    #         name
    #         type
    #         value
    #         error
    #     }
    #     }

    #     mutation StartPageFlow($request: KoiosStartPageflowRequest!) {
    #     data: startPageflow(request: $request) {
    #         ... on KoiosErrorResponse {
    #         code
    #         message
    #         errorFields
    #         }

    #         ... on KoiosStartPageflowSuccess {
    #         code
    #         pageflowId
    #         pageflowType

    #         page {
    #             id
    #             config
    #             elements {
    #             type
    #             componentType
    #             config
    #             field {
    #                 name
    #                 type
    #                 value
    #                 error
    #             }
    #             ...Children
    #             }
    #         }

    #         pageNum
    #         totalPages
    #         containerType
    #         config
    #         replyToken
    #         }
    #     }
    #     }
    # """

    # start_variables = {
    #     "request": {
    #         "name": "ContactBox-Rentals-Consumer-AskQuestion-v0.0.2",
    #         "context": {
    #         "_client": {
    #             "koiosClient": "koios.js v0.0.5",
    #             "deviceId": deviceId,
    #         },
    #         "rental_id": 4397849,
    #         # "rental": {
    #         #     "id": "4397849",
    #         #     "address": {
    #         #     "unit": "#A5",
    #         #     "__typename": "Address"
    #         #     },
    #         #     "listingAddress": "129 Franklin Street #A5",
    #         #     "listingPrice": "2095",
    #         #     "listingRooms": "2 rooms",
    #         #     "listingBeds": "1 bed",
    #         #     "listingBaths": "1 bath",
    #         #     "building": {
    #         #     "url": "https://streeteasy.com/building/129-franklin-street-jersey_city",
    #         #     "__typename": "Building"
    #         #     },
    #         #     "source": "Corcoran Sawyer Smith",
    #         #     "__typename": "Rental",
    #         #     "buildingLink": "https://streeteasy.com/building/129-franklin-street-jersey_city",
    #         #     "listedByList": [
    #         #     {
    #         #         "business_name": "Corcoran Sawyer Smith",
    #         #         "image": None,
    #         #         "industry_professional": {
    #         #         "headshot": None,
    #         #         "__typename": "IndustryProfessional"
    #         #         },
    #         #         "id": "346214",
    #         #         "is_pro": False,
    #         #         "name": "Preeti Poddar",
    #         #         "phone": "(201) 653-8000",
    #         #         "license": None,
    #         #         "__typename": "Contact"
    #         #     }
    #         #     ]
    #         # }
    #         },
    #         "fieldValues": {
    #             "name": "",
    #             "phone": "",
    #             "email": ""
    #         },
    #         "isStrict": False
    #     }
    # }

    # start_json_data = {
    #     "query": start_query,
    #     "variables": start_variables,
    # }

    # print(f'Trying POST {api_url}...')
    # time.sleep(random.randint(0, 3))
    # r = s.post(api_url, json=start_json_data, headers=headers)
    # print('Status code:', r.status_code, r.reason)
    # # print('JSON:', r.json())

    # pageflowId = r.json()['data']['data']['pageflowId']
    # replyToken = r.json()['data']['data']['replyToken']

    # print('pageflowId:', pageflowId)
    # print('replyToken:', replyToken)

    # finish_query = """
    #     mutation FinishPageflow($request: KoiosFinishPageflowRequest) {
    #         data: finishPageflow(request: $request) {
    #             ... on KoiosErrorResponse {
    #                 code
    #                 message
    #                 errorFields
    #             }

    #             ... on KoiosFinishPageflowSuccess {
    #                 code
    #                 returnConfig
    #             }
    #         }
    #     }
    # """

    # finish_variables = {
    #     "request": {
    #         "pageflowId": pageflowId,
    #         "replyToken": replyToken,
    #         "fieldValues": {
    #             "message": "message",
    #             "phone": "+12345678910",
    #             "search_partners": None,
    #             "email": "emailforpython@gmail.com",
    #             "name": "name"
    #         }
    #     }
    # }

    # finish_json_data = {
    #     "query": finish_query,
    #     "variables": finish_variables,
    # }

    # print(f'Trying POST {api_url}...')
    # r = s.post(api_url, json=finish_json_data, headers=headers)
    # print(f'Status code: {r.status_code} {r.reason}\n')
    # time.sleep(random.randint(0, 3))
    # print(r.json())


    # r = s.post(api_url, json=json_data, headers=headers)
    # # r = s.post(
    # #     url='https://proxy.scrapeops.io/v1/',
    # #     json=json_data,
    # #     headers=headers,
    # #     params={
    # #         'api_key': 'ff34d53e-11ae-48d1-8700-80a764a42210',
    # #         'url': api_url, 
    # #     },
    # # )

    # print('Status code:', r.status_code, r.reason)
    # # print('Headers:', r.headers)
    # print('returnConfig:', r.json()['data']['data']['returnConfig'])

    # print(script)









    # for url in [listing['url'] for listing in listings]:
    #     r = s.post(url, data=data)
    #     print('Status code:', r.status_code, r.reason)