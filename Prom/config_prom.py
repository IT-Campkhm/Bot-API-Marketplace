import os

TOKEN_PROM = os.environ.get('TOKEN_PROM')

URL_ORDER_LIST_PROM = 'https://my.prom.ua/api/v1/orders/list'
URL_SET_STATUS_PROM = 'https://my.prom.ua/api/v1/orders/set_status'
HEADERS_PROM = {
    'Authorization': f'Bearer {TOKEN_PROM}',
    'Cookie': 'cid=31787059051670770569459856278021553159',
    'Content-type': 'application/json'
}
PAYLOAD_PROM = {}
