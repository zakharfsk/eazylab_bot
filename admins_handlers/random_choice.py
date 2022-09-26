import random

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import Command
from loguru import logger

from config import OWNER, SECOND_MAN
from create_bot import bot
from database.models import Users


async def choice_winner(message: types.Message):
    try:

        users_ids = []

        for user in Users.select():
            users_ids.append(user)

        winners = []
        awards = [
            'виграв 2 відповіді на його вибір',
            'виграв 2 відповіді на його вибір',
            'виграв скидку 25% на відповіді',
            'виграв скидку 25% на відповіді',
            'виграв скидку 25% на відповіді'
        ]

        for i in range(5):
            winners.append(random.choice(users_ids))

        for i in range(len(winners)):

            winner: types.ChatMember = await bot.get_chat_member(winners[i], winners[i])

            if winner.user.id != OWNER and winner.user.id != SECOND_MAN:
                await message.answer(f'{winner.user.mention} {awards[i]}')

    except Exception as e:
        logger.exception(e)


def register_handlers_choice_winner(dp: Dispatcher):
    dp.register_message_handler(
        choice_winner,
        Command('choice_winner'),
        lambda message: OWNER == message.from_user.id or SECOND_MAN == message.from_user.id
    )
