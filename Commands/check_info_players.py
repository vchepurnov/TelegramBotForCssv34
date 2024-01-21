import asyncio
from datetime import datetime
from aiogram import types
from bs4 import BeautifulSoup
import requests
from check_spam import check_spam
import config

CHAT_BY_DATETIME = dict()

async def server_info(message:types.Message):
     # Время между сообщениями
    need_seconds = 1800
    current_time = datetime.now()
    # Время последнего сообщения
    last_datetime = CHAT_BY_DATETIME.get(message.chat.id)


    if check_spam(last_datetime, need_seconds, current_time):

        # Запрос на статус сервера
        page = requests.get(config.MonServer)
        # Запрос на текущих игроков сервера
        playes_page = requests.get(config.MonServerPlayers)

        # Парсинг ответов
        soup = BeautifulSoup(page.content, "html.parser")
        playes_page = requests.get(config.MonServerPlayers).text
        playes_online_soup = BeautifulSoup(playes_page, 'html.parser')
        tabl_players = playes_online_soup.find_all('div', class_="online-servers-players")
        
        # Получение информации из распарсинговых ответов
        players = soup.find(id="current_players")
        map = soup.find(id="current_maps")
        s1 = "  "
        s2 = "Никнейм       "
        s3 = "Фраги"
        s4 = " В игре "
        players_print = ""
        for player in tabl_players:
            string1 = (f"{player.find('div', class_='id').text}")
            string2 = (f"|{player.find('div', class_='player').text}")
            string3 = (f"|{player.find('div', class_='vip').text}")
            string4 = f"|{player.find('div', class_='time').text}"
            players_print += ('{:2}'.format(string1) +
                                '{:14.14}'.format(string2) +
                                '{:5}'.format(string3) +
                                '{:9.9}'.format(string4)+"\n")

        CHAT_BY_DATETIME[message.chat.id] = current_time
        return (f'<b>{config.PROJECTNAME}</b>'
                            f'\n<b>IP сервера:</b> <code>{config.IPServer}</code>'
                            f'\n<b>Карта:</b><i>{map.text}</i>'
                            f'\n<b>Кол-во игроков:</b> <i>{players.text}</i>'
                            f'\n<code>{s1}</code><code>{s2}</code><code>{s3}</code><code>{s4}</code>'
                            f'\n<code>{players_print}</code>')
    else:
        return ("Нельзя так часто использовать команду <b>'Информация'</b>")