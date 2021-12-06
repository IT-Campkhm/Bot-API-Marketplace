import asyncio
import json
import logging
import os
from datetime import datetime

import aiogram
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import Command

from globalconfig import CHAT_ID, MODER, OWNER
from Hubber.config import (HEADERS_HUBBER, URL_MESSAGE_HUBBER,
                        URL_ORDER_HUBBER, URL_SEND_MESSAGE_HUBBER)
from Hubber.HubberMessage import HubberMessage
from Hubber.HubberOrder import HubberOrder
from NovaPoshta.handler import NovaPoshta
from Prom.config import (HEADERS_PROM, PAYLOAD_PROM, URL_ORDER_LIST_PROM,
                        URL_SET_STATUS_PROM)
from Prom.PromOrder import Prom
from Rozetka.config import (HEADERS_ROZETKA, PAYLOAD_ROZETKA,
                            URL_ORDER_LIST_ROZETKA)
from Rozetka.RozetkaOrder import Rozetka
from HubberProvider.HubberProviderOrder import HubberProviderOrder
from HubberProvider.config import HEADERS_HUBBER_PROVIDER, URL_ORDER_PROVIDER_HUBBER

file_log = logging.FileHandler('log.txt')
console_log = logging.StreamHandler()
TOKEN = os.environ.get('TOKEN')


logging.basicConfig(handlers = (file_log, console_log), format = u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO)


bot = Bot(TOKEN, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot)


prom = Prom('Prom\key_order.txt')
rozetka = Rozetka('Rozetka\key_order.txt')
hubber = HubberOrder('Hubber\key_order.txt')
hubber_message = HubberMessage('Hubber\key_message.txt')
hubber_provider = HubberProviderOrder('HubberProvider\key_order.txt')
novaposhta = NovaPoshta()

async def on_startup_bot(dp: Dispatcher):
    try:

        if os.path.exists('Prom\key_order.txt'):
            order_prom = requests.request('GET', URL_ORDER_LIST_PROM, headers = HEADERS_PROM, data = PAYLOAD_PROM)
            p = open('Prom/key_order.txt', 'w')
            p.seek(0)
            p.write(str(order_prom.json()['orders'][0]['id']))
            p.close()
        else:
            logging.error('Файла Prom\key_order.txt немає')

        if os.path.exists('Rozetka\key_order.txt'):
            order_rozetka = requests.request('GET', URL_ORDER_LIST_ROZETKA, headers = HEADERS_ROZETKA, data = PAYLOAD_ROZETKA)
            r = open('Rozetka/key_order.txt', 'w')
            r.seek(0)

            if order_rozetka.json()['content']['orders'] != []:
                r.write(str(order_rozetka.json()['content']['orders'][0]['id']))
                r.close()
        else:
            logging.error('Файла Rozetka\key_order.txt немає')

        if os.path.exists('Hubber\key_order.txt'):
            order_hubber = requests.request('GET', URL_ORDER_HUBBER, headers = HEADERS_HUBBER, data = {})
            h = open('Hubber/key_order.txt', 'w')
            h.seek(0)
            h.write(str(order_hubber.json()[0]['id']))
            h.close()
        else:
            logging.error('Файла Hubber/key_order.txt немає')

        if os.path.exists('Hubber\key_message.txt'):
            message_hubber = requests.request('GET', URL_MESSAGE_HUBBER, headers = HEADERS_HUBBER, data = {})
            h_m = open('Hubber/key_message.txt', 'w')
            h_m.seek(0)
            h_m.write(str(message_hubber.json()[0]['id']))
        else:
            logging.error('Файла Hubber/key_message.txt немає')
        if order_rozetka.json()['content']['orders'] != []:
            await dp.bot.send_message(
                OWNER,
                'Запуск!\n'\
                f'Значення яке записалося в файл Prom/key_order.txt: {order_prom.json()["orders"][0]["id"]}\n'\
                f'Значення яке записалося в файл Rozetka/key_order.txt: {order_rozetka.json()["content"]["orders"][0]["id"]}\n\n'\
                f'Значення яке записалося в файл Hubber/key_order.txt: {order_hubber.json()[0]["id"]}\n'\
                f'Значення яке записалося в файл Hubber/key_message.txt: {message_hubber.json()[0]["id"]}\n\n'\
                f'Значеня з функції Rozetka.get_lastkey: {rozetka.get_lastkey()}\n'\
                f'Значеня з функції Prom.get_lastkey: {prom.get_lastkey()}\n'\
                f'Значеня з функції HubberOrder.get_lastkey: {hubber.get_lastkey()}\n'\
                f'Значеня з функції HubberMessage.het_lastkey: {hubber.get_lastkey()}'
            )
        else:
            await dp.bot.send_message(
                OWNER,
                'Запуск!\n'\
                f'Значення яке записалося в файл Prom/key_order.txt: {order_prom.json()["orders"][0]["id"]}\n'\
                f'Значення яке записалося в файл Rozetka/key_order.txt: {order_rozetka.json()["content"]["orders"]}\n\n'\
                f'Значення яке записалося в файл Hubber/key_order.txt: {order_hubber.json()[0]["id"]}\n'\
                f'Значення яке записалося в файл Hubber/key_message.txt: {message_hubber.json()[0]["id"]}\n\n'\
                f'Значеня з функції Rozetka.get_lastkey: {rozetka.get_lastkey()}\n'\
                f'Значеня з функції Prom.get_lastkey: {prom.get_lastkey()}\n'\
                f'Значеня з функції HubberOrder.get_lastkey: {hubber.get_lastkey()}\n'\
                f'Значеня з функції HubberMessage.het_lastkey: {hubber.get_lastkey()}'
            )

    except Exception as e:
        logging.exception(e)

@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    await dp.bot.send_message(
        OWNER,
        f'ID: {message.from_user.id}\n'\
        f'User name: {message.from_user.full_name}'
    )

@dp.message_handler(Command('send_log'))
async def log(message: types.Message):

    try:
        if message.from_user.id == OWNER:
            await dp.bot.send_document(OWNER, open(r'log.txt', 'rb'))
    except Exception as e:
        logging.exception(e)

@dp.message_handler(Command('test'))
async def _test(message: types.Message):

    try:
        await message.answer(f'{message}')
    except Exception as e:
        logging.exception(e)

@dp.message_handler(Command('test_pick'))
async def _test_pick(message: types.Message):
    try:
        await message.answer(
            'Клієнт '\
            f'<code>ПІБ</code>'\
            ' забрав свій(ої) товар(и):\n\n'\
            f'<code>Забрані товари</code>\n\n'\
            'Відправте технічний лист клієнту\n'
            f'Телефон: <code>Телефон кліжнта</code>\n'\
            f'TTN: \n'\
            f'Сервісне повідомлення: https://bit.ly/3krF2cN',
            disable_web_page_preview = True
        )
    except Exception as e:
        logging.exception(e)

@dp.message_handler(Command('get_id'))
async def _get_id(message: types.Message):
    try:
        await message.answer(
            f'{message.chat.id}'
        )
    except Exception as e:
        logging.exception(e)

@dp.message_handler(Command('keys'))
async def _keys(message: types.Message):
    if message.from_user.id == OWNER:

        with open('Prom/key_order.txt', 'r') as m:
            key_prom = m.read()

        with open('Rozetka/key_order.txt', 'r') as o:
            key_rozetka = o.read()

        with open('Hubber/key_order.txt', 'r') as h:
            key_hubber_order = h.read()

        with open('Hubber/key_message.txt') as h_m:
            key_hubber_message = h_m.read()

        await message.answer(
            f'Текуще значення в файлі Prom/key_order.txt: {key_prom}\n'\
            f'Текуще значення в файлі Rozetka/key_order.txt: {key_rozetka}\n\n'\
            f'Текуще значення в файлі Hubber/key_order.txt: {key_hubber_order}\n'\
            f'Текуще значення в файлі Hubber/key_message.txt: {key_hubber_message}\n\n'\
            f'Значеня з функції Rozetka.get_lastkey: {rozetka.get_lastkey()}\n'\
            f'Значеня з функції Prom.get_lastkey: {prom.get_lastkey()}\n'\
            f'Значеня з функції HubberOrder.get_lastkey: {hubber.get_lastkey()}\n'\
            f'Значеня з функції HubberMessage.het_lastkey: {hubber.get_lastkey()}'
        )

@dp.message_handler(Command('send'))
async def send_message(message: types.Message):
    try:
        if message.from_user.id in MODER:
            id_chat: int = message.text.split()[1]
            l = len(message.text.split())
            text_send: str = " ".join(message.text.split()[2:l])

            payload = json.dumps({
                "outgoing_id": id_chat,
                "message": text_send
            })

            response = requests.request('POST', URL_SEND_MESSAGE_HUBBER, headers = HEADERS_HUBBER, data = payload)

            now = datetime.now()

            for i in range(len(MODER)):
                await dp.bot.send_message(
                    MODER[i],
                    f'Відповів: {message.from_user.full_name}\n'\
                    f'ID чата: {response.json()["outgoing_id"]}\n'\
                    f'Повідомлення: {response.json()["message"]}\n\n'\
                    f'Час відправки: {now.strftime("%H:%M:%S %d.%B.%Y")}'
                )

    except Exception as e:
        logging.exception(e)

async def check_new_order_and_change_status_prom(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            logging.info('Перевірка на новий заказ на Prom')

            order = requests.request('GET', URL_ORDER_LIST_PROM, headers = HEADERS_PROM, data = PAYLOAD_PROM)
            new_order = prom.new_order()

            if new_order:
                payload = json.dumps({
                    'status': 'received',
                    'ids': [
                        order.json()['orders'][0]['id']
                    ]
                })

                change_status = requests.request('POST', URL_SET_STATUS_PROM, headers = HEADERS_PROM, data = payload)
                
                await dp.bot.send_message(
                    OWNER,
                    f'Заказ принятий на Prom({change_status.status_code})'
                )

                prom.update_lastkey(order.json()['orders'][0]['id'])
            
        except Exception as e:
            logging.exception(e)

async def check_new_order_and_change_status_rozetka(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        
        try:
            logging.info('Перевірка на новий заказ на Rozetka')

            new_order = rozetka.new_order()
            responce = requests.request('GET', URL_ORDER_LIST_ROZETKA, headers = HEADERS_ROZETKA, data = PAYLOAD_ROZETKA)
            
            if new_order:

                payload = json.dumps({
                    'status': 26,
                    'seller_comment': 'Autho status'
                })

                change_status = requests.request('PUT', f'https://api-seller.rozetka.com.ua/orders/{responce.json()["content"]["orders"][0]["id"]}', headers = HEADERS_ROZETKA, data = payload)

                await dp.bot.send_message(
                    OWNER,
                    f'Заказ принятий на розетці({change_status.status_code})'
                )                
                
                rozetka.update_lastkey(responce.json()['content']['orders'][0]['id'])

        except Exception as e:
            logging.exception(e)

async def check_new_order_hubber(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            response = requests.request('GET', URL_ORDER_HUBBER, headers = HEADERS_HUBBER, data = {})

            logging.info('Пройшла перевірка на новий заказ Hubber')

            new_order = hubber.new_order()

            if new_order:
                for i in range(len(MODER)):
                    await dp.bot.send_message(
                        MODER[i],
                        '<b>Поступив новий заказ</b>\n\n'\
                        f'ID заказа: {response.json()[0]["alias"]}\n'
                        f'Статус заказа: {response.json()[0]["status"]["title"]}\n'\
                        f'Ім\'я та прізвище клієнта: {response.json()[0]["outgoing"][0]["client_name"]}\n'\
                        f'Номер телефона клієнта: {response.json()[0]["outgoing"][0]["client_phone"]}\n'\
                        f'Емаїл клієнта: {response.json()[0]["outgoing"][0]["client_email"]}\n'\
                        f'Постачальник: {response.json()[0]["outgoing"][0]["company"]["title"]}\n'\
                        f'Доставка: {response.json()[0]["outgoing"][0]["delivery_data"]}\n'\
                        f'Нотатки до замовлення: {response.json()[0]["outgoing"][0]["order_notes"]}\n\n'\
                        '<b>Товар</b>\n'\
                        f'ID товара: {response.json()[0]["outgoing"][0]["products"][0]["vendor_code"]}\n'\
                        f'Назва товара: {response.json()[0]["outgoing"][0]["products"][0]["title"]}\n'\
                        f'Ціна за одну штуку: {response.json()[0]["outgoing"][0]["products"][0]["price"]}\n'\
                        f'Кількість: {response.json()[0]["outgoing"][0]["products"][0]["count"]}\n\n'\
                        f'<a href = \'https://office.hubber.pro/order/edit/{response.json()[0]["id"]}\'>Більше інформації</a>'
                    )
                
                hubber.update_lastkey(response.json()[0]['id']) #Оновлення ключа
        
        except Exception as e:
            logging.exception(e)

async def check_new_message_hubber(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            response = requests.request('GET', URL_MESSAGE_HUBBER, headers = HEADERS_HUBBER, data = {})

            logging.info('Перевірка на нове повідомлення Hubber')

            new_message = hubber_message.new_messages()

            if new_message:
                for i in range(len(MODER)):
                    await dp.bot.send_message(
                        MODER[i],
                        f'Нове повідомлення від поставщика <b>{response.json()[0]["company"]}</b>\n'\
                        f'ID повідомлення: {response.json()[0]["id"]}\n'\
                        f'ID чата: {response.json()[0]["outgoing_id"]}\n'\
                        f'Компанія: {response.json()[0]["company"]}\n\n'\
                        f'Повідомлення: {response.json()[0]["message"]}\n'\
                        f'Відправлено: {response.json()[0]["created_at"]}'
                    )
                hubber_message.update_lastkey(response.json()[0]['id']) #Оновлення ключа
        except Exception as e:
            logging.exception(e)

async def check_novaposhta(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            order_complete = novaposhta.general_function()

            if order_complete:

                l = len(order_complete[1]['content']['orders'][order_complete[2]]['items_photos'])

                item = []

                for items in range(l):
                    item.append(order_complete[1]['content']['orders'][order_complete[2]]['items_photos'][items]['item_name'])

                i = '\n'.join(item)
                
                await dp.bot.send_message(
                    CHAT_ID,
                    'Клієнт '\
                    f'<code>{order_complete[1]["content"]["orders"][order_complete[2]]["recipient_title"]["full_name"]}</code>'\
                    ' забрав свій(ої) товар(и):\n\n'\
                    f'<code>{i}</code>\n\n'\
                    'Відправте технічний лист клієнту\n'
                    f'Телефон: {order_complete[1]["content"]["orders"][order_complete[2]]["recipient_phone"]}\n'\
                    f'TTN: {order_complete[1]["content"]["orders"][order_complete[2]]["ttn"]}\n'\
                    f'Сервісне повідомлення: https://bit.ly/3krF2cN',
                    disable_web_page_preview = True
                )

                await dp.bot.send_message(
                    OWNER,
                    'Клієнт '\
                    f'<code>{order_complete[1]["content"]["orders"][order_complete[2]]["recipient_title"]["full_name"]}</code>'\
                    ' забрав свій(ої) товар(и):\n\n'\
                    f'<code>{i}</code>\n\n'\
                    'Відправте технічний лист клієнту\n'
                    f'Телефон: {order_complete[1]["content"]["orders"][order_complete[2]]["recipient_phone"]}\n'\
                    f'TTN: {order_complete[1]["content"]["orders"][order_complete[2]]["ttn"]}\n'\
                    f'Сервісне повідомлення: https://bit.ly/3krF2cN',
                    disable_web_page_preview = True
                )
                
        except Exception as e:
            logging.exception(e)
            await dp.bot.send_message(
                OWNER,
                f'{e}'
            )

async def check_new_order_hubber_provider(wait_for):
    try:
        while True:
            await asyncio.sleep(wait_for)

            logging.info('Пройшла перевірка на новий заказ Hubber Provider')

            new_order = hubber_provider.new_order()

            if new_order:
                response = requests.request('GET', URL_ORDER_PROVIDER_HUBBER, headers = HEADERS_HUBBER_PROVIDER, data = {})
                print(len(response.json()['products']))
                for i in range(len(MODER)):
                    await dp.bot.send_message(
                        MODER[i],
                        '<b>Наш товар заказали на маркетплейсі</b>\n\n'\
                        f'ID заказа: {response.json()[0]["alias"]}\n'
                        f'Статус заказа: {response.json()[0]["status"]["title"]}\n'\
                        f'Ім\'я та прізвище клієнта: {response.json()[0]["client_name"]}\n'\
                        f'Номер телефона клієнта: {response.json()[0]["client_phone"]}\n'\
                        f'Емаїл клієнта: {response.json()[0]["client_email"]}\n'\
                        f'Маркетплейс: {response.json()[0]["company"]["title"]}\n'\
                        f'Доставка: {response.json()[0]["delivery_data"]}\n'\
                        f'Нотатки до замовлення: {response.json()[0]["comment"]}\n\n'\
                        '<b>Товар</b>\n'\
                        f'ID товара: {response.json()[0]["products"][0]["vendor_code"]}\n'\
                        f'Назва товара: {response.json()[0]["products"][0]["title"]}\n'\
                        f'Ціна за одну штуку: {response.json()[0]["products"][0]["price"]}\n'\
                        f'Кількість: {response.json()[0]["products"][0]["count"]}\n'\
                        f'Комісія в %: {response.json()[0]["products"][0]["supplier_commission_percent"]}\n'\
                        f'Комісія в грн: {response.json()[0]["products"][0]["supplier_commission_money"]}'
                    )
                
                hubber_provider.update_lastkey(response.json()[0]['id']) #Оновлення ключа

    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    
    #asyncio.get_event_loop().create_task(check_new_order_and_change_status_prom(3))
    #asyncio.get_event_loop().create_task(check_new_order_and_change_status_rozetka(10))
    
    #asyncio.get_event_loop().create_task(check_new_order_hubber(20))
    #asyncio.get_event_loop().create_task(check_new_message_hubber(25))
    asyncio.get_event_loop().create_task(check_new_order_hubber_provider(30))

    #asyncio.get_event_loop().create_task(check_novaposhta(200))

    executor.start_polling(dp, on_startup = on_startup_bot)
