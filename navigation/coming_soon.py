from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


async def coming_soon(message: types.Message):
    await message.answer('Хей. Скоро появляться й інши предмети з яких ти зможеш замовити готову домашку ^^')


def register_handlers_coming_soon(dp: Dispatcher):
    dp.register_message_handler(coming_soon, Text(equals='Coming soon...'))
