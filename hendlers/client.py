from aiogram import types, Dispatcher

from collections import defaultdict
import json

from config import CHANNEL_ID, BOT_ADMIN_ID
from create_bot import dp


di = defaultdict(int)
flag = 0


# @dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.reply('Здесь есть эта команда, только потому что это база')


# @dp.message_handler()
# async def answer_for_roma(message: types.Message):
#     with open('database/curse_words.txt', encoding='utf-8') as curse_file:
#         for word in message.text.split(' '):
#             if word in curse_file.read():
#                 await message.reply('+')
#

# start counting messages
# @dp.message_handler(commands=['start_counting'])
async def start_message_counting(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        global flag
        flag = 1
        await message.reply('Я начал записывать статистику')


# stop counting messages
# @dp.message_handler(commands=['stop_counting'])
async def stop_command(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        global flag
        flag = 0
        await message.reply('Я закончил записывать статистику')
        with open('database/data.json', 'w', encoding='utf-8') as file:
            print(json.load(file))
            json.dump(di, file)


async def counting_text_message(message: types.Message):
    global flag
    if flag == 1: # and message.chat.id == CHANNEL_ID
        di[f'{message.from_user.first_name} ({message.from_user.username}), text'] += 1


async def counting_voice_message(message: types.Message):
    global flag
    if flag == 1:
        di[f'{message.from_user.first_name} ({message.from_user.username}) voice'] += 1


# declare message handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(start_message_counting, commands=['start_cnt'])
    dp.register_message_handler(stop_command, commands=['stop_cnt'])
    dp.register_message_handler(counting_text_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(counting_voice_message, content_types=types.ContentType.VOICE)
