import os

API_TOKEN_HUBBER = os.environ.get('API_TOKEN_HUBBER')

HEADERS_HUBBER = {
    'Authorization': f'Bearer {API_TOKEN_HUBBER}',
    'Content-type': 'application/json'
}

URL_ORDER_HUBBER = 'http://office.hubber.pro/api/v1/order'
URL_MESSAGE_HUBBER = 'http://office.hubber.pro/api/v1/order/messages'
URL_SEND_MESSAGE_HUBBER = 'https://office.hubber.pro/api/v1/order/send-message'