import logging
import json
from collections import defaultdict
from aiogram import executor, Bot, Dispatcher, types
from config import TOKEN, CHANNEL_ID, BOT_ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

di = defaultdict(int)


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.reply('Здесь есть эта команда, только потому что это база')


# start counting messages
@dp.message_handler(commands=['start_counting'])
async def start_message_counting(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        di['flag'] = 1
        await message.reply('Я начал записывать статистику')


# stop counting messages
@dp.message_handler(commands=['stop_counting'])
async def stop_command(message: types.Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.reply('Ты не мой Одмин')
    else:
        di['flag'] = 0
        await message.reply('Я закончил записывать статистику')
        with open('data.json', 'a', encoding='utf-8') as file:
            json.dump(di, file)


# func for show message statistic
@dp.message_handler()
async def test(message: types.Message):
    print(type(message.photo))


@dp.message_handler()
async def counting_message(message: types.Message):
    if di['flag'] == 1 and message.chat.id == CHANNEL_ID:
        di[f'{message.from_user.first_name} ({message.from_user.username})'] += 1

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)