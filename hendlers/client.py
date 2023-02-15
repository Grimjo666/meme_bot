from aiogram import types, Dispatcher
from create_db import get_message_stats


async def start_command(message: types.Message):
    await message.reply('Здесь есть эта команда, только потому что это база')


async def show_message_stats(message: types.Message):
    data = get_message_stats()
    statistic_text = ''
    for item in data:
        statistic_text += f'{item[1]} ({item[2]}) отправил {item[3] + item[4] + item[7]} сообщений, из них:\n\n'
        statistic_text += f'-- {item[3]} текстовых, общей длинной {item[5]} символов\n'
        statistic_text += f'-- {item[4]} голосовых, общей длиной {item[6]} секунд\n'
        statistic_text += f'-- {item[7]} стикер(в)\n*3'
    await message.answer(statistic_text)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(show_message_stats, commands=['show_stats'])
