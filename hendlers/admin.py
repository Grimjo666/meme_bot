from aiogram import types, Dispatcher
from collections import defaultdict

from config import CHANNEL_ID, BOT_ADMIN_ID

from create_db import writing_info_to_bd


flag = 0


# Старт сбора статистики
async def start_message_counting(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        global flag
        flag = 1
        await message.reply('Я начал записывать статистику')


# Сбор статистики сообщений
async def counting_text_message(message: types.Message):
    global flag
    if flag == 1: # and message.chat.id == CHANNEL_ID
        writing_info_to_bd(message.from_user.id, message.from_user.first_name, message.from_user.username, text_count=1, len_all_text=len(message.text))


async def counting_voice_message(message: types.Message):
    global flag
    if flag == 1:
        writing_info_to_bd(message.from_user.id, message.from_user.first_name, message.from_user.username, voice_count=1, len_all_voice=message.voice.duration)


# Прекращение сбора статистики
async def stop_command(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        global flag
        flag = 0
        await message.reply('Я закончил записывать статистику')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_message_counting, commands=['start_cnt'])
    dp.register_message_handler(stop_command, commands=['stop_cnt'])
    dp.register_message_handler(counting_voice_message, content_types=types.ContentType.VOICE)
    dp.register_message_handler(counting_text_message, content_types=types.ContentType.TEXT)

