import json
import logging
from datetime import datetime

import requests
from Rozetka.config import (HEADERS_ROZETKA, PAYLOAD_ROZETKA,
                            URL_ORDER_LIST_ROZETKA)

from NovaPoshta.config import API_TOKEN_NP, HEADERS_NOVAPOSHTA, URL_TRACKING_NP
from globalconfig import STATUS


class NovaPoshta:
    url_rozetka_order = URL_ORDER_LIST_ROZETKA
    url_headers_rozetka = HEADERS_ROZETKA
    url_rozetka_payload = PAYLOAD_ROZETKA
    url_novaposhta_tracking = URL_TRACKING_NP
    token_np = API_TOKEN_NP

    def get_order_list_rozetka(self):
        try:
            return requests.request('GET', self.url_rozetka_order + '?ttn=1', headers = self.url_headers_rozetka, data = self.url_rozetka_payload).json()
        except Exception as e:
            logging.exception(e)

    def get_order_by_ttn(self, ttn):
        try:
            return requests.request('GET', f'https://api-seller.rozetka.com.ua/orders/search?ttn={ttn}', headers = HEADERS_ROZETKA, data = {})
        except Exception as e:
            logging.exception(e)

    def end(self, *args):
        return args

    def general_function(self):
        try:

            if self.get_order_list_rozetka()['success'] and self.get_order_list_rozetka()['content']['orders'] is not None:

                logging.info('Перевірка на зміну статуса в НП и Розетці')
                logging.info(f"{len(self.get_order_list_rozetka()['content']['orders'])}")

                for order in range(len(self.get_order_list_rozetka()['content']['orders'])):

                    payload = json.dumps({
                        "apiKey": "7a0c6342493be713667a16e5b9d152f6",
                        "modelName": "TrackingDocument",
                        "calledMethod": "getStatusDocuments",
                        "methodProperties": {
                            "Documents": [
                                {
                                    "DocumentNumber": f"{self.get_order_list_rozetka()['content']['orders'][order]['ttn']}",
                                    "Phone": f"{self.get_order_list_rozetka()['content']['orders'][order]['recipient_phone']}"
                                }
                            ]
                        }
                    })

                    nova = requests.request('POST', self.url_novaposhta_tracking, headers = HEADERS_NOVAPOSHTA, data = payload)

                    logging.info(f'{nova.json()["data"][0]["Status"]}')
                    logging.info(f'{type(nova.json()["data"][0]["StatusCode"])}')

                    if int(nova.json()['data'][0]['StatusCode']) in STATUS:
                        
                        order_by_ttn = self.get_order_by_ttn(self.get_order_list_rozetka()['content']['orders'][order]['ttn'])
                        logging.info(f'{order_by_ttn.json()["content"]["orders"][order]["items_photos"][0]["item_name"]}')
                        self.end(True, order_by_ttn.json(), order)
                        '''
                        payload_rozetka = json.dumps({
                            'status': 6,
                            'seller_comment': 'Autho status. '\
                                                f'Buyer picked up at {datetime.now().strftime("%d.%M.%Y %H:%M:%S")}'
                        })
                        finaly = requests.request('PUT', f'https://api-seller.rozetka.com.ua/orders/{order_by_ttn.json()["content"]["orders"][order]["id"]}', headers = HEADERS_ROZETKA, data = payload_rozetka)
                        '''

        except Exception as e:
            logging.exception(e)
