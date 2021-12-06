import os

API_TOKEN_HUBBER_PROVIDER = os.environ.get('API_TOKEN_HUBBER_CANOE5')

HEADERS_HUBBER_PROVIDER = {
    'Authorization': f'Bearer {API_TOKEN_HUBBER_PROVIDER}',
    'Content-type': 'application/json'
}

URL_ORDER_PROVIDER_HUBBER = 'http://office.hubber.pro/api/v1/outgoing'