from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
import config

main_buttons = ReplyKeyboardMarkup(
	keyboard = [
		[
            KeyboardButton(text="Информация")
		],
	],
	resize_keyboard=True
)

connectgame = InlineKeyboardMarkup()
connectgame.add(InlineKeyboardButton(text="Сайт",url=config.Site))