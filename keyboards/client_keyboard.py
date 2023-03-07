from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_back_to_main_menu = InlineKeyboardButton(text='В основное меню', callback_data='btn_back_to_main_menu')
button_close_menu = InlineKeyboardButton(text='Закрыть', callback_data='btn_close')

# Основное меню бота
ikb_main_menu = InlineKeyboardMarkup(row_width=1)

button_info = InlineKeyboardButton(text='Информация', callback_data='info_btn')
button_weather = InlineKeyboardButton(text='Погода', callback_data='weather_btn')
button_message_stat = InlineKeyboardButton(text='Статистика сообщений', callback_data='message_stat_btn')

ikb_main_menu.add(button_info, button_weather, button_message_stat, button_close_menu)


# Меню, при нажатии на кнопку "Информация"
info_menu = InlineKeyboardMarkup(row_width=2)

button_creator_info = InlineKeyboardButton(text='Создатель бота', url='tg://user?id=888175079')
button_bot_info = InlineKeyboardButton(text='Информация о боте', callback_data='bot_info_btn')

info_menu.add(button_creator_info, button_bot_info)
info_menu.add(button_back_to_main_menu)
info_menu.add(button_close_menu)


# Меню, при нажатии на кнопку "Информация о боте"
bot_info_text = InlineKeyboardMarkup(row_width=1).add(button_back_to_main_menu, button_close_menu)

# Меню, при нажатии на кнопку "погода"
weather_menu = InlineKeyboardMarkup(row_width=1)

button_weather_today = InlineKeyboardButton(text='Погода на сегодня', callback_data='btn_weather_today')
button_weather_3days = InlineKeyboardButton(text='Погода на 3 дня', callback_data='btn_weather_3days')
button_weather_5days = InlineKeyboardButton(text='Погода на 5 дней', callback_data='btn_weather_5days')

weather_menu.add(button_weather_today,
                 button_weather_3days,
                 button_weather_5days,
                 button_back_to_main_menu,
                 button_close_menu)


# Меню, при нажатии на кнопу "погода (временной промежуток)"
weather_interval = InlineKeyboardMarkup(row_width=1)

button_send_locate = InlineKeyboardButton(text='Погода по местоположению', callback_data='btn_send_locate')
button_choice_locate = InlineKeyboardButton(text='Ввести город в ручную', callback_data='btn_city_input')

weather_interval.add(button_send_locate,
                     button_choice_locate,
                     button_back_to_main_menu,
                     button_close_menu)
