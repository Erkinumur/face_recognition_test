from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from facecontrolapp.bot.loader import dp
from facecontrolapp.bot.utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))
