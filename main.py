# Default modules - Модули по умолчанию
import csv
import random 
from os import system
from time import sleep
from datetime import datetime

# Downloaded libraries - Скачанные библиотеки
import requests
# import logging
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton 

# Created module - Созданный модуль
from core.config import TOKEN, ADMIN_ID, WEATHER_IP
from core.weather import weather_city 
from core.static.sticker import STICKER_001 

system("clear")

bot = Bot(token = TOKEN) 
dp = Dispatcher(bot)

# with open(f"core/admin/data/UserInfo.csv", "a", encoding = "UTF - 8") as file:
#     writer = csv.writer(file)
#     ID = "ID"
#     USERNAME = "USERNAME"
#     FIRST_NAME = "FIRST_NAME"
#     LAST_NAME = "LAST_NAME"
#     PHONE = "PHONE"
#     writer.writerow([ID, USERNAME, FIRST_NAME, LAST_NAME, PHONE]) 
 
@dp.message_handler(commands = ["start"])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True).add(
        KeyboardButton("Зарегистрироваться", request_contact = True) 
    )
    photo_start = open("core/static/image/1130701.jpg", "rb")
    await message.answer_photo(photo = photo_start, caption = "Привет я бот. Для пользования пройдите регистрацию:", reply_markup = markup)
    # await message.answer("Привет я бот. Для пользования пройдите регистрацию: ") 

@dp.message_handler(content_types = types.ContentType.CONTACT)
async def contact_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True).add(
        KeyboardButton("Алматы"), KeyboardButton("Астана"), KeyboardButton("Атырау"),
        KeyboardButton("Караганды"), KeyboardButton("Шымкент"), KeyboardButton("Актау"),
        KeyboardButton("Петропавловск")

    )
    user_id = message.contact.user_id
    username = message.chat.username
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number 

    with open(f"core/admin/data/UserInfo.csv", "a", encoding = "UTF - 8") as file:
        writer = csv.writer(file)
        
        writer.writerow(
            (
                user_id,
                username,
                first_name,
                last_name,
                phone
            )
        )
        Informations = f"""id: {user_id}
username: @{username}
first_name: {first_name}
last_name: {last_name}
phone: {phone}
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """

        registration_photo = open("core/static/image/1130701.jpg", "rb")
        await bot.send_photo(ADMIN_ID, registration_photo, Informations)
        await message.answer("Вы успешно зарегистрированы, теперь отправьте название любого города: ", reply_markup = markup)

    message_count = []
    @dp.message_handler(content_types = ["text"])
    async def weather_city_author (message: types.Message):
        get_weather_def = weather_city(message.text)
        message_count.append(random.randint(0, 1))
        await message.reply(get_weather_def)

        if len(message_count) >= 3:
            await message.reply_sticker(random.choice(STICKER_001))
            message_count.clear()

if __name__ == "__main__":
    print("Бот запущен")
    executor.start_polling(dp)



