import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
import json

TOKEN = ""

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#parsing
data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()


#First contact with user
@dp.message_handler(commands=["start","help"])
async def start_message(message: types.Message):
	but1 = types.KeyboardButton("💵Курсы валют💶")
	but2 = types.KeyboardButton("Об авторе")
	keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
	keyboard1.add(but1).add(but2)
	await message.answer("Добрый день или вечер\nВыбери нужную кнопку", reply_markup=keyboard1)

#Currency
@dp.message_handler()
async def get_values(message: types.Message):
	if message.text=="💵Курсы валют💶":
		but1 = types.InlineKeyboardButton(text="USD",callback_data="usd")
		but2 = types.InlineKeyboardButton(text="EUR", callback_data="eur")
		keyboard2 = types.InlineKeyboardMarkup(width=2)
		keyboard2.add(but1, but2)
		await message.answer("Выберите валюту", reply_markup=keyboard2)
	elif message.text=="Об авторе":
		await message.answer("Меня зовут Максим, я начинающий разработчик на Python🐍.\nЭто мой первый бот курсов валют, который выдаёт самый точный результат с сайта ЦБ.\nМоя телега ---> @Iuskiue")
	else:
		await message.answer("Выбери нужную команду!")	

	

#Printing USD
@dp.callback_query_handler(text="usd")
async def get_usd(call: types.CallbackQuery):
	await call.message.answer("💵 На сегодня курс равен "+str(data['Valute']['USD']["Value"])+" рубля. \n💵 Недавно курс был "+str(data['Valute']['USD']["Previous"])+" рубля.")

#Printing EUR
@dp.callback_query_handler(text="eur")
async def get_usd(call: types.CallbackQuery):
	await call.message.answer("💶 На сегодня курс равен "+str(data['Valute']['EUR']["Value"])+" рубля. \n💶 Недавно курс был "+str(data['Valute']['EUR']["Previous"])+" рубля.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

