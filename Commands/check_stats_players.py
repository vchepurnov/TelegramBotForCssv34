import asyncio
from datetime import datetime
from aiogram import types
from bs4 import BeautifulSoup
import requests
from check_spam import check_spam
import config

CHAT_BY_DATETIME = dict()

async def topplayers(message:types.Message):
    # Время между сообщениями
    need_seconds = 5
    # Время последнего сообщения
    last_stats_datetime = CHAT_BY_DATETIME.get(message.chat.id)
    current_time = datetime.now()
    
    # Проверяем на наличе отправленого сообщения
    if check_spam(last_stats_datetime, need_seconds, current_time):
        # Парсинг ответов
        stats_page = requests.get(config.Hlstats)
        stats_page_soup = BeautifulSoup(stats_page.content, 'lxml')  
        s1 = '  '
        s2 = ' Никнейм     '
        s3 = ' Опыт'
        stats_print = ""
        trs_tabl_stats = stats_page_soup.find_all('tr',limit=11) [1:]
        for tr in trs_tabl_stats:
            tds = tr.find_all('td')
            string1 = f"{tds[0].getText()}"
            string2 = f"|{tds[1].getText()}"
            string3 = f"|{tds[2].getText()}"
            stats_print += ('{:2}'.format(string1) +
                            '{:14.14}'.format(string2) +
                            '{:7}'.format(string3) + "\n")
        CHAT_BY_DATETIME[message.chat.id] = datetime.now()
        return (f'<b>[ ДОСУГ ] Лучшие игроки:</b>\n'
                            f'\n<code>{s1}</code><code>{s2}</code><code>{s3}</code>'
                            f'\n<code>{stats_print}</code>')
    else:
        return ("Нельзя так часто использовать команду <b>'Топ 10'</b>")
