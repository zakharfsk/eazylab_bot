import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from loguru import logger

from create_keyboards.keyboards import start_menu


async def back_to_menu(message: types.Message):
    try:
        await message.answer(
            'Ти в головному меню.',
            reply_markup=start_menu()
        )

    except Exception as e:
        logger.exception(e)


def register_handlers_back_to_menu(dp: Dispatcher):
    dp.register_message_handler(back_to_menu, Text(equals='Назад в меню'))
