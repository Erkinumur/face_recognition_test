from aiogram import types
from facecontrolapp.bot.loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
