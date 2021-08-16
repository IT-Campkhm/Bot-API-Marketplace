import logging
import os

import requests

from Hubber.config import HEADERS_HUBBER, URL_MESSAGE_HUBBER


class HubberMessage:
    url = URL_MESSAGE_HUBBER
    headers = HEADERS_HUBBER
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file
        
        if(os.path.exists(lastkey_file)):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(str(self.lastkey))
            f.close()

    def new_messages(self):
        try:
            response = requests.request("GET", self.url, headers = self.headers, data = {})
            new = []
            data = response.json()

            logging.info(f'Lastkey: {self.lastkey}, New Message.py')
            logging.info(f'ID: {data[0]["id"]}, New Message.py')
            logging.info(f'New: {new}, New Message.py')

            if int(self.lastkey) != int(data[0]['id']):
                new.append(data[0]['id'])
                return new
            else:
                logging.info('Else newnessage.py\n\n')
                
        except Exception as e:
            logging.exception(e)

    def get_lastkey(self):
        response = requests.request("GET", self.url, headers = self.headers, data = {})
        data = response.json()

        return data[0]['id']

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        logging.info(f'Ключ оновлений {new_key}')

        with open(self.lastkey_file, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key
