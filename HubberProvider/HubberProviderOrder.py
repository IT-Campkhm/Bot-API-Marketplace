import logging
import os

import requests

from HubberProvider.config import HEADERS_HUBBER_PROVIDER, URL_ORDER_PROVIDER_HUBBER

class HubberProviderOrder:
    url = URL_ORDER_PROVIDER_HUBBER
    headers = HEADERS_HUBBER_PROVIDER
    lastkey_file = ''
    lastkey = ''

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(str(self.lastkey))
            f.close()

    def new_order(self):
        try:
            response = requests.request("GET", self.url, headers = self.headers, data = {})
            new = []
            data = response.json()

            logging.info(f'Lastkey: {self.lastkey}, New Order')
            logging.info(f'ID: {data[0]["id"]}, New Order')
            logging.info(f'New: {new}, New Order')
            
            if int(self.lastkey) != int(data[0]['id']):
                new.append(data[0]['id'])
                print(new)
                return new
            else:
                logging.info('Else neworder.py\n\n')
        
        except Exception as e:
            logging.exception(e)

    def get_lastkey(self):
        response = requests.request("GET", self.url, headers = self.headers, data = {})
        data = response.json()

        return data[0]["id"]
        
    def update_lastkey(self, new_key):
        self.lastkey = new_key

        logging.info(f'Ключ оновлений {new_key}')

        with open(self.lastkey_file, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key