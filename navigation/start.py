import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from config import OWNER
from create_bot import bot
from create_keyboards.keyboards import start_menu
from database.db import User


async def _start_command(message: types.Message, state: FSMContext):
    try:

        user_db = User()

        if user_db.get_user_by_id(message.from_user.id) is None and message.from_user.is_bot is False:
            user_db.add_new_user(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name
            )
            await bot.send_message(
                OWNER,
                'Новий користувач бота\n'
                f'ID: {message.from_user.id}\n'
                f'Username: {message.from_user.username}\n'
                f'First Name: {message.from_user.first_name}\n'
                f'Last Name: {message.from_user.last_name}'
            )

        await message.answer(
            'Привіт!\n'
            'З допомогою цього бота ти замовиш Лабораторні роботи. 🥰🥰🥰\n\n'
            'Як правильно оформлювати закази можна подивитися в головному меню, '
            'нажавши на кнопку <b>Інструкція використання</b>\n'
            'Якщо заказ буде оформлений не по шаблону, він розглядатися не буде. Дякуємо за розуміння! 😊😊😊',
            reply_markup=start_menu()
        )
        del user_db
        await state.reset_state(with_data=True)
    except Exception as e:
        logging.exception(e)


def register_handlers_start_command(dp: Dispatcher):
    try:
        dp.register_message_handler(_start_command, Command('start'), state="*")
    except Exception as e:
        logging.exception(e)
