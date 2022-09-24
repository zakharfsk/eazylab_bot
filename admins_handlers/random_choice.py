import logging
import random

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import Command

from config import OWNER, SECOND_MAN
from create_bot import bot
from database.db import User


async def choice_winner(message: types.Message):
    try:

        user_db = User()
        users_ids = user_db.get_all_users()

        winners = []
        awards = [
            'виграв 2 відповіді на його вибір',
            'виграв 2 відповіді на його вибір',
            'виграв скидку 25% на відповіді',
            'виграв скидку 25% на відповіді',
            'виграв скидку 25% на відповіді'
        ]

        for i in range(5):
            winners.append(random.choice(users_ids)[0])

        for i in range(len(winners)):

            winner: types.ChatMember = await bot.get_chat_member(winners[i], winners[i])

            if winner.user.id != OWNER and winner.user.id != SECOND_MAN and winner.user.id != ENGLISH_MAN_1 and winner.user.id != ENGLISH_MAN_2:
                await message.answer(f'{winner.user.mention} {awards[i]}')

        del user_db

    except Exception as e:
        logging.exception(e)


def register_handlers_choice_winner(dp: Dispatcher):
    try:
        dp.register_message_handler(
            choice_winner,
            Command('choice_winner'),
            lambda message: OWNER == message.from_user.id or SECOND_MAN == message.from_user.id
        )
    except Exception as e:
        logging.exception(e)
