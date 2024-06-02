from .config import get_field_values
from .database import insert_new_listing
from .utility import try_post

field_values = get_field_values()

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


def get_pageflow_id(listing_id, s):
    start_variables['request']['context']['rental_id'] = listing_id

    start_json_data = {
        'query': start_query,
        'variables': start_variables,
    }

    r = try_post(api_url, start_json_data, 'get_pageflow_id', s)

    pageflow_id = r.json()['data']['data']['pageflowId']
    reply_token = r.json()['data']['data']['replyToken']

    print('pageflowId:', pageflow_id)
    print('replyToken:', reply_token)

    return pageflow_id, reply_token


def submit_message(pageflow_id, reply_token, s):
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

    try_post(api_url, finish_json_data, 'submit_message', s)


def send_messages(listings, s):
    for listing in listings:
        pageflow_id, reply_token = get_pageflow_id(listing['listing_id'], s)
        submit_message(pageflow_id, reply_token, s)
        insert_new_listing(listing)
