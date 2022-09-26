import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from loguru import logger

from config import subject_buttons
from create_keyboards.keyboards import subject_keyboard


async def see_price(message: types.Message):
    try:
        await message.answer(
            'Вибири нище потрібний предмет ⬇',
            reply_markup=subject_keyboard(subject_buttons).add('Назад в меню')
        )

    except Exception as e:
        logger.exception(e)


def register_handlers_see_price(dp: Dispatcher):
    dp.register_message_handler(see_price, Text(equals='👨‍🏫 Подивитися прайс'))
