import logging

from create_bot import dp
from aiogram import executor

from hendlers import client, admin

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот вышел в онлайн')


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
