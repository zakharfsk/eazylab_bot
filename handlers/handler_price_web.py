import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from loguru import logger

from config import web_buttons, OWNER
from create_bot import bot


async def web_lab(message: types.Message):
    try:
        owner: types.ChatMember = await bot.get_chat_member(OWNER, OWNER)
        await message.answer(
            'Хей. А ось і прайс лист для Вашої Лабораторної роботи, будем раді вашому замовлені ^^\n\n'
            '<code>Вся Лабораторна - 800грн</code>\n\n'
            f'Якщо вас цікавить тільки якась частина, тоді пишить - {owner.user.mention} (для замовлення також)'
        )
    except Exception as e:
        logger.exception(e)


async def web_pract(message: types.Message):
    try:
        owner: types.ChatMember = await bot.get_chat_member(OWNER, OWNER)
        await message.answer(
            'Хей. А ось і прайс лист для Вашої Практичної роботи, будем раді вашому замовлені ^^\n\n'
            '<code>'
            'Лабораторна №1 - 150грн\n'
            'Лабораторна №2 - 150грн\n'
            'Лабораторна №3 - 200грн\n'
            'Лабораторна №4 - 150грн\n'
            'Лабораторна №5 - 200грн\n'
            'Лабораторна №6 - 250грн\n'
            'Лабораторна №7 - 400грн\n'
            'Лабораторна №8 - 350грн\n'
            'Лабораторна №9 - 400грн'
            '</code>\n\n'
            f'Для замовлення пишить - {owner.user.mention}'
        )
    except Exception as e:
        logger.exception(e)


def register_message_handler_web(dp: Dispatcher):
    dp.register_message_handler(
        web_lab,
        Text(equals=web_buttons[0])
    )

    dp.register_message_handler(
        web_pract,
        Text(equals=web_buttons[1])
    )
