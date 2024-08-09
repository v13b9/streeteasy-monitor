from .utils import get_datetime


class Messager:
    api_url = 'https://api-v6.streeteasy.com/'

    pageflow_variables = {
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

    pageflow_query = """
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

    message_query = """
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
            print(f'{get_datetime()}\nNew listing: {listing['address']}')
            try:
                print('Sending message...')
                pageflow_id, reply_token = self.get_pageflow_id(listing['listing_id'])
                if self.submit_message(pageflow_id, reply_token):
                    print('Message sent successfully\n')
                    self.db.insert_new_listing(listing)
                else:
                    print('Error sending message: Failed to submit message\n')
            except Exception as e:
                print(f'Error sending message: {e}\n')

    def submit_message(self, pageflow_id, reply_token):
        message_variables = {
            'request': {
                'pageflowId': pageflow_id,
                'replyToken': reply_token,
                'fieldValues': self.field_values,
            }
        }

        payload = {
            'query': Messager.message_query,
            'variables': message_variables,
        }

        r = self.session.post(Messager.api_url, json=payload)
        if r.status_code == 200:
            return True
        return False

    def get_pageflow_id(self, listing_id):
        Messager.pageflow_variables['request']['context']['rental_id'] = listing_id
        payload = {
            'query': Messager.pageflow_query,
            'variables': Messager.pageflow_variables,
        }

        r = self.session.post(Messager.api_url, json=payload)

        pageflow_id = r.json()['data']['data']['pageflowId']
        reply_token = r.json()['data']['data']['replyToken']

        return pageflow_id, reply_token
