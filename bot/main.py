
import os
import shelve
import pathlib
import sqlite3
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from functions import *

TG_TOKEN = os.getenv("TG_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button = types.KeyboardButton("Отправить геолокацию",
                                  request_location=True)

session = 'session'

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hажми на 📎, сделай фото банкноты \
                        и отправь его в бот!",
                        reply_markup=keyboard.add(button))

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def save_photo(message: types.Message):

    """
    user_session.tg_session_info['dt'] = dt
    user_session.tg_session_info['datetime'] = dt.strftime('20%y%m%d%H%M%S')
    """

    dt = datetime.now()
    duser_session = User_Session()
    chat_info = message.chat
    msge_info = {'message_id': message.message_id,
                 'date': message.date,
                 'caption': message.caption}
    user_info = message.from_user
    foto_info = message.photo[-1]
    file_info = await bot.get_file(message.photo[-1].file_id)


    user_session.get_tg_msge_info(msge_info)
    user_session.get_tg_chat_info(chat_info)
    user_session.get_tg_user_info(user_info)
    user_session.get_tg_foto_info(foto_info)
    user_session.get_tg_file_info(file_info)

    session_dir = session + '/' + str(user_session.tg_user_info['id'])
    pathlib.Path(session_dir).mkdir(parents=True, exist_ok=True)

    file_name = get_file_name(user_session.tg_file_info['file_path'])
    user_session.tg_file_info['file_name'] = file_name

    file_extension = get_file_extension(user_session.tg_file_info['file_path'])
    user_session.tg_file_info['file_extension'] = file_extension

    download_file_name = session_dir + '/' + file_name
    user_session.file_path['file_path'] = pathlib.Path(download_file_name)

    await bot.download_file(file_info.file_path,
                            download_file_name)

    file_hash = get_file_hash(download_file_name)
    file_hash_path = session_dir + '/' + file_hash
    user_session.tg_file_info['file_hash'] = file_hash

    user_session.file_path['file_path'].replace(file_hash_path)
    with shelve.open(session_dir + '/database') as db:
        db.update({file_hash: user_session})
    """
    await message.reply(dict(user_session.tg_chat_info))
    await message.reply(dict(user_session.tg_msge_info))
    await message.reply(dict(user_session.tg_user_info))
    await message.reply(dict(user_session.tg_foto_info))
    await message.reply(dict(user_session.tg_file_info))
    """
    await message.reply("Нажми на кнопку, чтобы отправить свою геолокацию")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await message.answer(f"latitude: {latitude}")
    await message.answer(f"longitude: {longitude}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
