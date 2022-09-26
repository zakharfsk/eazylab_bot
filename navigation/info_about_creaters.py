from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from loguru import logger


async def informations(message: types.Message):
    try:
        await message.answer(
            'Привіт ми раді, що ви користуєтеся нашим ботом. 🥰\n'
            'Цього бота й ідею розробили двоє студентів, яким завжди не хватало на каву ^^\n\n'
            f'Розобник бота - Holo4ka.\n'
            f'Допоміг з розвитком ідеї - Fisvif.'
        )

    except Exception as e:
        logger.exception(e)


def register_handlers_informations(dp: Dispatcher):
    dp.register_message_handler(informations, Text(equals='ℹ️ Інформація'))
