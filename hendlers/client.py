from aiogram import types, Dispatcher
from create_db import get_message_stats_from_db

from collections import defaultdict



async def start_command(message: types.Message):
    await message.reply('Здесь есть эта команда, только потому что это база')


async def send_message_info(message: types.Message):
    data = get_message_stats_from_db()
    statistic_text = ''
    for item in data:
        statistic_text += f'{item[1]} ({item[2]}) отправил {item[3] + item[4] + item[7]} сообщений, из них:\n\n'
        statistic_text += f'-- {item[3]} текстовых, общей длинной {item[5]} символов\n'
        statistic_text += f'-- {item[4]} голосовых, общей длиной {item[6]} секунд\n'
        statistic_text += f'-- {item[7]} стикер(в)\n*3'
    await message.answer(statistic_text)


# Функция, отправляющая пользователю диаграмму статистики сообщений
async def send_message_diagram(message: types.Message):
    data = get_message_stats_from_db()
    all_mes_dict = defaultdict(int)
    diagram = ''
    # Проходимся по списку с инфой о пользователе,
    # забираем имя, ник, кол-во сообщений текстовых, голосовых и стикеров
    for _, name, username, text_c, voice_c, _, _, sticker_c in data:
        all_mes_dict[f'{name} ({username})'] = text_c + voice_c + sticker_c

    count_all_messages = sum(all_mes_dict.values())

    # Собираем диаграмму для отправки пользователю
    for person, num in sorted(all_mes_dict.items(), key=lambda x: x[1], reverse=True)[:5]:

        # Находим процент активности в чате для каждого пользователя
        percent = round(num / count_all_messages * 100) // 10
        if percent == 0:
            percent = 1

        diagram += f'{person}: {"🔸" * percent}\n'
    await message.answer(diagram)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(send_message_info, commands=['show_stats_info'])
    dp.register_message_handler(send_message_diagram, commands=['show_dg'])

