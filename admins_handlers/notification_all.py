import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked
from loguru import logger

from config import OWNER, SECOND_MAN, CHAT
from create_bot import bot
from create_keyboards.keyboards import start_menu
from database.models import Users


class SendMessageAllUsers(StatesGroup):
    start_sendings = State()


async def input_text_for_message(message: types.Message, state: FSMContext):
    try:
        await SendMessageAllUsers.start_sendings.set()
        await message.reply(
            'Ведіть текст для розсилки',
            reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена розсилки')
        )
    except Exception as e:
        logger.exception(e)


async def cancel_send_message_all_users(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.reset_state(with_data=True)

        await message.reply(
            'Розсилка зупинена',
            reply_markup=start_menu()
        )

    except Exception as e:
        logger.exception(e)


async def send_text_all_users(message: types.Message, state: FSMContext):
    try:
        message_for_sending = message.text

        await message.answer(
            'Розсилка почалась. Очікуйте повідомлення про її закінчення.',
            reply_markup=start_menu()
        )

        for person in Users.select():
            try:
                await bot.send_message(
                    person.user_id,
                    f'{message_for_sending}'
                )
                await asyncio.sleep(0.3)
            except BotBlocked:
                Users.delete().where(Users.user_id == person.user_id)
                await message.answer(f'Видалено: {person.user_id}')

        info_about_sending = await bot.send_message(
            CHAT,
            f'Повідомлення було надіслане {len(Users.select())} користувачам бота\n\n'
            f'Текст повідомлення:\n{message_for_sending}',
        )

        await bot.pin_chat_message(
            CHAT,
            info_about_sending.message_id,
            disable_notification=False
        )
        await state.reset_state(with_data=True)

    except Exception as e:
        logger.exception(e)


def register_handlers_rozsilaca_messages(dp: Dispatcher):
    dp.register_message_handler(input_text_for_message, Command('rozsilca'),
                                lambda message: OWNER == message.from_user.id or SECOND_MAN == message.from_user.id)
    dp.register_message_handler(cancel_send_message_all_users,
                                Text(equals='Отмена розсилки'),
                                state="*")
    dp.register_message_handler(send_text_all_users,
                                state=SendMessageAllUsers.start_sendings)
