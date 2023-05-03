from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database.create_db import get_message_stats_from_db
from other.diagram import create_dg
from create_bot import bot
from other.weather import city_cord, get_weather_dict

# Импорты клавиатур
from keyboards.client_keyboard import ikb_main_menu, weather_menu_ikb, weather_interval_ikb
from keyboards.client_keyboard import info_menu_ikb, bot_info_text_ikb, statistic_message_ikb

from collections import defaultdict


# Создаем класс состояний меню
class MenuState(StatesGroup):
    main_menu = State()
    info = State()
    weather = State()
    weather_interval = State()
    weather_city_input = State()
    statistic = State()


# Отправляем основное меню
async def cmd_menu(message: types.Message, state: FSMContext):
    await message.answer('Меню бота:', reply_markup=ikb_main_menu)
    await state.set_state(MenuState.main_menu)


# _________________________________ Блок инфо хэндлеров _________________________________

# Обработчик для кнопки "Информация о боте"
async def info_btn_handler(callback_query, state):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Информация:',
                                reply_markup=info_menu_ikb)
    await state.set_state(MenuState.info)


# Обработчик для кнопки "Создатель бота"
async def bot_info_handler(callback_query):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Мне пока что впадлу придумывать сюда описание',
                                reply_markup=bot_info_text_ikb)


# _________________________________ Блок инфо хэндлеров _________________________________


# _______________________________ Блок погодных хэндлеров _______________________________
# Обработчик для кнопки "Погода"
async def weather_btn_handler(callback_query, state):
    # Присылаем погодное меню
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Погодное меню:',
                                reply_markup=weather_menu_ikb)
    await state.set_state(MenuState.weather)


# Обработчик для кнопки "Погода (и временной промежуток)"
async def weather_interval_handler(callback_query, state):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Дайте доступ к своим гео данным или введите город в ручную',
                                reply_markup=weather_interval_ikb)

    await state.update_data(count_weather_days=callback_query.data)
    await state.set_state(MenuState.weather_interval)


# получение геолокации пользователя
async def get_location(callback_query):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Я пока что не понимаю как получить геоданные')


# Проси пользователя ввести город
async def input_city_name(callback_query, state):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Введи название города\nК примеру: "Москва"',
                                reply_markup=None)

    await state.set_state(MenuState.weather_city_input)


# _______________________________ Блок погодных хэндлеров _______________________________

# ______________________________ Блок хэндлеров статистики ______________________________
# Обработчик для кнопки "Статистика сообщений"
async def send_statistic_menu(callback_query, state):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Меню статистики',
                                reply_markup=statistic_message_ikb)
    await state.set_state(MenuState.statistic)


# Функция, отправляющая пользователю статистику сообщений
async def send_message_info(callback_query, state):
    data = get_message_stats_from_db()
    statistic_text = ''
    for item in data:
        statistic_text += f'{item[1]} ({item[2]}) отправил {int(item[3]) + int(item[4]) + int(item[7])} сообщений, из них:\n\n'
        statistic_text += f'-- {item[3]} текстовых, общей длинной {item[5]} символов\n'
        statistic_text += f'-- {item[4]} голосовых, общей длиной {item[6]} секунд\n'
        statistic_text += f'-- {item[7]} стикер(в)\n\n\n'

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=statistic_text,
                                reply_markup=None)
    await state.finish()


# Функция, отправляющая пользователю диаграмму статистики сообщений
async def send_message_diagram(message, state):
    data = get_message_stats_from_db()
    all_mes_dict = defaultdict(int)
    diagram = ''
    # Проходимся по списку с инфой о пользователе,
    # забираем имя, ник, кол-во сообщений текстовых, голосовых и стикеров
    for _, name, username, text_c, voice_c, _, _, sticker_c in data:
        all_mes_dict[f'{name} / {username}'] = int(text_c) + int(voice_c) + int(sticker_c)

    count_all_messages = sum(all_mes_dict.values())
    person_percents = []
    # Собираем диаграмму для отправки пользователю
    for person, num in sorted(all_mes_dict.items(), key=lambda x: x[1], reverse=True)[:5]:

        # Находим процент активности в чате для каждого пользователя
        percent = round(num / count_all_messages * 100) // 10
        if percent == 0:
            percent = 1
        person_percents.append((person, num))

    # Создаём диаграмму на основе собранных выше данных и отправляем её
    create_dg.create_diagram(person_percents)
    with open('other/diagram/statistic_person_activ.png', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)

# ______________________________ Блок хэндлеров статистики ______________________________


# Хэндлер для обработки нажатий на кнопки в main_menu
async def process_callback_main_menu(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'info_btn':
        await info_btn_handler(callback_query, state)
    elif data == 'weather_btn':
        await weather_btn_handler(callback_query, state)
    elif data == 'message_stat_btn':
        await send_statistic_menu(callback_query, state)
    elif data == 'btn_close':
        await close_menu(callback_query, state)


# Хэндлер для обработки нажатий на кнопки в info menu
async def process_callback_info_menu(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'bot_info_btn':
        await bot_info_handler(callback_query)
    elif data == 'btn_back_to_main_menu':
        await close_menu(callback_query, state)
        await cmd_menu(callback_query.message, state)
    elif data == 'btn_close':
        await close_menu(callback_query, state)


# Хэндлер для обработки нажатий на кнопки weather menu
async def process_callback_weather_menu(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data

    if data in ('btn_weather_today', 'btn_weather_3days', 'btn_weather_5days'):
        await weather_interval_handler(callback_query, state)
    elif data == 'btn_back_to_main_menu':
        await close_menu(callback_query, state)
        await cmd_menu(callback_query.message, state)
    elif data == 'btn_close':
        await close_menu(callback_query, state)


# Хэндлер для обработки нажатий на кнопки в подменю в weather menu
async def process_callback_weather_interval_menu(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data

    if data == 'btn_send_locate':
        await get_location(callback_query)
    elif data == 'btn_city_input':
        await input_city_name(callback_query, state)
    elif data == 'btn_back_to_main_menu':
        await close_menu(callback_query, state)
        await cmd_menu(callback_query.message, state)
    elif data == 'btn_close':
        await close_menu(callback_query, state)


# Хэндлер получения города от пользователя и отправки ему погоды в этом городе
async def send_weather_by_name(message: Message, state: FSMContext):

    state_data = await state.get_data()
    callback_data = state_data.get('count_weather_days')

    async def send_weather(num, message_from_user, step=1, mes=message, st=state):
        for date, info in weather_data[:num:step]:

            hour = int(date.split()[1][:2])  # Получаем час прогноза

            if hour > 19 or hour < 6:
                message_from_user += f'📅 {date} 🌙\n\n {info}\n\n\n'
            else:
                message_from_user += f'📅 {date} ☀\n\n {info}\n\n\n'
        await mes.answer(message_from_user)
        await st.finish()

    try:
        weather_data = get_weather_dict(city_cord(message.text))

        if callback_data == 'btn_weather_today':
            await send_weather(6, 'Погода на ближайшие 15 часов\n\n')

        elif callback_data == 'btn_weather_3days':
            await send_weather(24,'Погода на ближайшие 3 дня\n\n',  step=4)

        elif callback_data == 'btn_weather_5days':
            await send_weather(40,'Погода на ближайшие 5 дней\n\n', step=8)

    except Exception as exc:
        await message.answer('Вы ввели не корректный город или что то с сервером погоды')
        await state.finish()
        print('Ошибка при получении словаря погоды:', exc)


# Хэндлер для отправки статистики
async def process_callback_statistics_menu(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'btn_show_stats':
        await send_message_info(callback_query, state)
    elif data == 'btn_show_diagram':
        await send_message_diagram(callback_query.message, state)
    elif data == 'btn_back_to_main_menu':
        await close_menu(callback_query, state)
        await cmd_menu(callback_query.message, state)
    elif data == 'btn_close':
        await close_menu(callback_query, state)


# Обработчик для кнопки "Закрыть"
async def close_menu(callback, state):
    message = callback.message
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=message.message_id,
                                        reply_markup=None)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_menu, commands=['menu', 'start', 'help'])
    dp.register_callback_query_handler(process_callback_main_menu, state=MenuState.main_menu)
    dp.register_callback_query_handler(process_callback_info_menu, state=MenuState.info)
    dp.register_callback_query_handler(process_callback_weather_menu, state=MenuState.weather)
    dp.register_callback_query_handler(process_callback_weather_interval_menu, state=MenuState.weather_interval)
    dp.register_message_handler(send_weather_by_name, state=MenuState.weather_city_input)
    dp.register_callback_query_handler(process_callback_statistics_menu, state=MenuState.statistic)
    dp.register_message_handler(send_message_diagram, commands=['show_dg'])
