from aiogram import types, Dispatcher


# @dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.reply('Здесь есть эта команда, только потому что это база')


# declare message handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])


