import logging
import os

import requests

from Rozetka.config import (HEADERS_ROZETKA, PAYLOAD_ROZETKA,
                                    URL_ORDER_LIST_ROZETKA)


class Rozetka:
    url = URL_ORDER_LIST_ROZETKA
    headers = HEADERS_ROZETKA
    payload = PAYLOAD_ROZETKA
    lastkey = ''
    lastkey_file = ''

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file
        
        if(os.path.exists(lastkey_file)):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(str(self.lastkey))
            f.close()

    def __repr__(self) -> str:
        return 'Перевірка на нові замовлення'

    def new_order(self):
        try:

            response = requests.request('GET', self.url, headers = self.headers, data = self.payload)
            new = []

            logging.info(f'Lastkey: {self.lastkey}, New Order')
            
            if response.json()['content']['orders'] != []:
                logging.info(f'ID: {response.json()["content"]["orders"][0]["id"]}, New Order')
            
            logging.info(f'New: {new}, New Order')
            logging.info(
                f'\n{response.json()["content"]["orders"]}\n'\
                f'{response.json()["content"]["orders"] == []}\n'\
                f'{self.lastkey == None}'
                )
            
            if self.lastkey is not None and int(self.lastkey) != int(response.json()['content']['orders'][0]['id']) and response.json()['content']['orders'] != []:
                new.append(response.json()['content']['orders'][0]['id'])
                return new
            else:
                if os.path.exists('Rozetka\key_order.txt'):
                    order_rozetka = requests.request('GET', URL_ORDER_LIST_ROZETKA, headers = HEADERS_ROZETKA, data = PAYLOAD_ROZETKA)
                    r = open('Rozetka/key_order.txt', 'w')
                    r.seek(0)
                    if order_rozetka.json()['content']['orders'] != []:
                        r.write(str(order_rozetka.json()['content']['orders'][0]['id']))
                        r.close()
                logging.info('Else neworder.py\n\n')
        
        except Exception as e:
            logging.exception(e)


    def get_lastkey(self):
        response = requests.request("GET", self.url, headers = self.headers, data = self.payload)
        if response.json()['content']['orders']:
            return response.json()['content']['orders'][0]['id']

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key
