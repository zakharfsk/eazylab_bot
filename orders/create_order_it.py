import uuid

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger

from config import OWNER, ADMIN_CHAT, \
    select_object_buttons, it_buttons, CHAT
from create_bot import bot
from create_keyboards.keyboards import subject_keyboard, start_menu, cancel_keyboard, it_keyboard
from database.models import OrderIt


class Order(StatesGroup):
    waiting_subject = State()
    waiting_number_lab_it = State()
    waiting_first_last_name = State()
    waiting_user_group = State()


async def start_order(message: types.Message, state: FSMContext):
    try:
        await state.update_data(customer_id=message.from_user.id, order_id=int(uuid.uuid4().fields[-1]))
        await Order.waiting_subject.set()
        await message.reply('Виберіть предмет.', reply_markup=subject_keyboard(select_object_buttons).add('Отмена'))
    except Exception as e:
        logger.exception(e)


async def cancel_order(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.reset_state(with_data=True)

        await message.reply(
            'Вихід з створення заказу\n'
            'Вас перенаправлено в головне меню',
            reply_markup=start_menu()
        )

    except Exception as e:
        logger.exception(e)


async def input_subject(message: types.Message, state: FSMContext):
    try:
        subject = message.text

        if subject in select_object_buttons:
            await state.update_data(select_object=subject)
            await Order.next()
            await message.reply('Виберіть лабораторну з ІТ.', reply_markup=it_keyboard().add('Отмена'))
        else:
            await message.reply(
                'Упсс...\n'
                'Нажаль такого предмета немає'
            )
    except Exception as e:
        logger.exception(e)


async def input_number_lab_it(message: types.Message, state: FSMContext):
    try:
        number_lab = message.text

        if number_lab in it_buttons:
            await state.update_data(number_lab=number_lab)
            await message.reply('Вкажіть ваше Ім\'я та Прізвище.', reply_markup=cancel_keyboard())
            await Order.next()

        else:
            await message.reply(
                'Упс...\n'
                'Нажаль в нас немає такої Лабораторної'
            )

    except Exception as e:
        logger.exception(e)


async def input_name(message: types.Message, state: FSMContext):
    try:
        name = message.text
        await state.update_data(name=name)
        await Order.next()
        await message.reply('Вкажіть вашу групу.(в форматі КІ-21-2)')
    except Exception as e:
        logger.exception(e)


async def input_group(message: types.Message, state: FSMContext):
    try:
        user_group = message.text
        payments: types.ChatMember = await bot.get_chat_member(OWNER, OWNER)

        await state.update_data(user_group=user_group)
        data = await state.get_data()

        await message.reply(
            'Дякуємо за замовлення. Скоро звами зв\'яжуться наші менеджери',
            reply_markup=start_menu()
        )

        if message.from_user.id != OWNER:
            OrderIt.create(
                id_customer=data.get('customer_id'),
                id_order=data.get('order_id'),
                name_object=data.get('select_object'),
                number_lab=data.get('number_lab'),
                first_name_and_last_name=data.get('name'),
                user_group=data.get('user_group')
            )

        await message.answer(
            'Ваш чек.\n\n'
            f'ID заказа: {data["order_id"]}\n'
            f'ID замовника: {data["customer_id"]}\n'
            f'Username: {message.from_user.username}\n'
            f'First Name: {message.from_user.first_name}\n'
            f'Last Name: {message.from_user.last_name}\n'
            f'Вказане І\'мя та Прізвище: {data["name"]}\n'
            f'Предмет: {data["select_object"]}\n'
            f'Номер лабораторної: {data["number_lab"]}\n'
            f'Група: {data["user_group"]}\n\n'
            'Час виконання: 1-2 дня\n'
            f'Щоб оплатити зверніться до {payments.user.mention}'
        )

        await bot.send_message(
            CHAT,
            f'ID заказа: {data["order_id"]}\n'
            f'ID замовника: {data["customer_id"]}\n'
            f'Username: {message.from_user.username}\n'
            f'First Name: {message.from_user.first_name}\n'
            f'Last Name: {message.from_user.last_name}\n'
            f'Вказане І\'мя та Прізвище: {data["name"]}\n'
            f'Предмет: {data["select_object"]}\n'
            f'Номер лабораторної: {data["number_lab"]}\n'
            f'Група: {data["user_group"]}'
        )

        await state.reset_state(with_data=True)

    except Exception as e:
        logger.exception(e)


def register_handlers_create_it(dp: Dispatcher):
    dp.register_message_handler(start_order, Text(equals='💸 Зробити замовлення'), state=None)
    dp.register_message_handler(cancel_order, state="*", commands=['back'])
    dp.register_message_handler(cancel_order, Text(equals='Отмена'), state="*")
    dp.register_message_handler(input_subject, Text(equals='Інформаціїні технології'),
                                state=Order.waiting_subject)
    dp.register_message_handler(input_number_lab_it, state=Order.waiting_number_lab_it)
    dp.register_message_handler(input_name, state=Order.waiting_first_last_name)
    dp.register_message_handler(input_group, state=Order.waiting_user_group)
