import asyncio
import requests
from Commands.check_info_players import server_info
import config
import kbs
import db

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from bs4 import BeautifulSoup
from Commands.check_stats_players import topplayers

bot = Bot(config.API_TOKEN,parse_mode='html') 
dp = Dispatcher(bot,storage=MemoryStorage())
CHAT_BY_DATETIME = dict()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await db.users(message.from_user.id)
    await message.answer(f'Добро пожаловать.\nЭто оффициальный бот проекта {config.PROJECTNAME}', reply_markup=kbs.main_buttons)

@dp.message_handler(text='Информация')
async def infoserv(message:types.Message):
    info_message = await server_info(message)
    info_mes = await message.answer (info_message)

    await asyncio.sleep(1800)
    try:
        await info_mes.delete() 
        await message.delete()
    except Exception as e:
        pass

@dp.message_handler(text='Топ 10')
async def show_topplayers(message:types.Message):

    stat_message = await topplayers(message)
    stats_mes = await message.answer (stat_message)

    await asyncio.sleep(1800)
    try:
        await stats_mes.delete() 
        await message.delete()
    except Exception as e:
        pass

executor.start_polling(dp)