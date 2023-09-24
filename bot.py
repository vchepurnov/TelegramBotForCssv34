from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import asyncio
import config
import kbs
import db

bot = Bot(config.API_TOKEN,parse_mode='HTML') 
dp = Dispatcher(bot,storage=MemoryStorage())
CHAT_BY_DATETIME = dict()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await db.users(message.from_user.id)
    await message.answer(f'Добро пожаловать.\nЭто оффициальный бот проекта {config.PROJECTNAME}', reply_markup=kbs.main_buttons)

@dp.message_handler(text='Информация')
async def infoserv(message:types.Message):
    need_seconds = 10
    current_time = datetime.now()
    last_datetime = CHAT_BY_DATETIME.get(message.chat.id)

    # Если первое сообщение (время не задано)
    if not last_datetime:
        CHAT_BY_DATETIME[message.chat.id] = current_time
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
        await message.answer (f'<b>[v34] ДОСУГ [Public] 18+</b>'
                            f'\n<b>IP сервера:</b> <code>{config.IPServer}</code>'
                            f'\n<b>Карта:</b><i>{map.text}</i>'
                            f'\n<b>Кол-во игроков:</b> <i>{players.text}</i>'
                            f'\n<code>{s1}</code><code>{s2}</code><code>{s3}</code><code>{s4}</code>'
                            f'\n<code>{players_print}</code>')
        await asyncio.sleep(10)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await infoserv.delete()
        except Exception as e:
            pass
    else:
        # Разница в секундах между текущим временем и временем последнего сообщения
        delta_seconds = (current_time - last_datetime).total_seconds()

        # Осталось ждать секунд перед отправкой
        seconds_left = int(need_seconds - delta_seconds)

        # Если время ожидания не закончилось
        if seconds_left > 0:
           await message.answer ("Нельзя так часто использовать команду <b>'Информация'</b>")
        else:
            CHAT_BY_DATETIME[message.chat.id] = current_time
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
            await message.answer (f'<b>[v34] ДОСУГ [Public] 18+</b>'
                                f'\n<b>IP сервера:</b> <code>{config.IPServer}</code>'
                                f'\n<b>Карта:</b><i>{map.text}</i>'
                                f'\n<b>Кол-во игроков:</b> <i>{players.text}</i>'
                                f'\n<code>{s1}</code><code>{s2}</code><code>{s3}</code><code>{s4}</code>'
                                f'\n<code>{players_print}</code>')
            await asyncio.sleep(10)
                # на всякий случай проверяем есть ли еще сообщение
            try:
                await infoserv.delete()
            except Exception as e:
                pass

executor.start_polling(dp)