from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import Command
from loguru import logger

from config import OWNER
from database.models import Users, OrderProgramming, OrderEnglish, OrderHigherMath, OrderIt


async def test_func(message: types.Message):
    try:
        logger.info('Users DB')
        for person in Users.select():
            logger.info(person)

        logger.info('OrderProgramming DB')
        for person in OrderProgramming.select():
            logger.info(person)

        logger.info('OrderEnglish DB')
        for person in OrderEnglish.select():
            logger.info(person)

        logger.info('OrderHigherMath DB')
        for person in OrderHigherMath.select():
            logger.info(person)

        logger.info('OrderIt DB')
        for person in OrderIt.select():
            logger.info(person)
    except Exception as e:
        logger.exception(e)


def register_handlers_test(dp: Dispatcher):
    dp.register_message_handler(test_func, Command('test'), lambda message: OWNER == message.from_user.id)
