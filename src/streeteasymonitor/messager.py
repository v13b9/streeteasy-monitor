from .utility import get_datetime

class Messager:
    api_url = 'https://api-v6.streeteasy.com/'

    start_variables = {
        'request': {
            'name': 'ContactBox-Rentals-Consumer-AskQuestion-v0.0.2',
            'context': {
                '_client': {
                    'koiosClient': 'koios.js v0.0.5',
                },
            },
            'isStrict': False,
        }
    }

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

    def __init__(self, monitor, listings):
        self.field_values = monitor.config.get_field_values()
        self.session = monitor.session
        self.db = monitor.db
        self.listings = listings

    def send_messages(self):
        for listing in self.listings:
            print(f'{get_datetime()} New listing: {listing['address']}')
            try:
                print(f'Sending message...')
                pageflow_id, reply_token = self.get_pageflow_id(listing['listing_id'])
                if self.submit_message(pageflow_id, reply_token):
                    print(f'Message sent successfully')
                    self.db.insert_new_listing(listing)
                else:
                    print(f'Error sending message: Failed to submit message')
            except Exception as e:
                print(f'Error sending message: {e}')

    def submit_message(self, pageflow_id, reply_token):
        finish_variables = {
            'request': {
                'pageflowId': pageflow_id,
                'replyToken': reply_token,
                'fieldValues': self.field_values,
            }
        }

        finish_json_data = {
            'query': self.finish_query,
            'variables': finish_variables,
        }

        r = self.session.post(self.api_url, json=finish_json_data)
        if r.status_code == 200:
            return True
        return False

    def get_pageflow_id(self, listing_id):
        self.start_variables['request']['context']['rental_id'] = listing_id
        start_json_data = {
            'query': self.start_query,
            'variables': self.start_variables,
        }

        r = self.session.post(self.api_url, json=start_json_data)

        pageflow_id = r.json()['data']['data']['pageflowId']
        reply_token = r.json()['data']['data']['replyToken']

        # print('pageflowId:', pageflow_id)
        # print('replyToken:', reply_token)

        return pageflow_id, reply_token
