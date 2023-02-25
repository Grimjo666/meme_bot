from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_back_to_main_menu = InlineKeyboardButton(text='В основное меню', callback_data='btn_back_to_main_menu')

# Основное меню бота
ikb_main_menu = InlineKeyboardMarkup(row_width=1)

info_button = InlineKeyboardButton(text='Информация о боте', callback_data='info_btn')
weather_button = InlineKeyboardButton(text='Погода', callback_data='weather_btn')
message_stat_button = InlineKeyboardButton(text='Статистика сообщений', callback_data='message_stat_btn')

ikb_main_menu.add(info_button, weather_button, message_stat_button)


# Меню, при нажатии на кнопку "погода"
weather_menu = InlineKeyboardMarkup(row_width=1)

button_weather_today = InlineKeyboardButton(text='Погода на сегодня', callback_data='btn_weather_today')
button_weather_3days = InlineKeyboardButton(text='Погода на 3 дня', callback_data='btn_weather_3days')
button_weather_5days = InlineKeyboardButton(text='Погода на 5 дней', callback_data='btn_weather_5days')


weather_menu.add(button_weather_today, button_weather_3days, button_weather_5days, button_back_to_main_menu)
