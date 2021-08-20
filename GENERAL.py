import logging
import requests
import os
import json


class General:
    
    LOGIN = os.environ.get('LOGIN_ROZETKA')
    PASSWORD = os.environ.get('PASSWORD_ROZETKA')
    PAYLOAD = json.dumps({
        "username": f"{LOGIN}",
        "password": f"{PASSWORD}"
    })
    HEADERS = {
        'Content-Type': 'application/json',
        'Cookie': 'PHPSESSID=a0kl1dpiv2eh4qsah855phbj73; _csrf=d0e636efc62a47a4ac6a569e97a8554590740a69e9ceeffffbac6d72493b8c93a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Xd1sHqhLoOWgo52mRof0OFT6PNWADSS6%22%3B%7D'
    }

    def login_rozetka(self):
        response = requests.request('POST', self.URL_AUTHORIZATION, headers = self.HEADERS, data = self.PAYLOAD)
        TOKEN = f'{response.json()["content"]["access_token"]}'

        return {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json',
            'Cookie': 'PHPSESSID=a9r0afnr1tc7eab5jl1aptqpnj; _csrf=e02b40f2dbdc5c50765d3fbd94cecdca8b08db717c06a7a39d33af0734a829b4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22b6AJJ4fevoRZWcNuuthYCe1DwH-gh0PD%22%3B%7D'
        }