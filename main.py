import logging
import os

from aiogram import executor, types, Bot, Dispatcher
from loguru import logger

from database.models import db, __all__
from config import OWNER
from create_bot import dp, bot

from handlers import *
from navigation import *
from admins_handlers import *
from orders import *

logger.add(
    "file.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
    level="DEBUG",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# ------------------------------Handlers-------------------------------------- #

handler_price_programming.register_handlers_price_programming(dp)
handler_price_IT.register_handlers_price_IT(dp)
handler_price_hight_math.register_handlers_price_hight_math(dp)
handler_price_english.register_message_handler_english(dp)
handler_price_web.register_message_handler_web(dp)

# ------------------------------Navigation-------------------------------------- #

look_price.register_handlers_see_price(dp)
start.register_handlers_start_command(dp)
choose_lab.register_handlers_choose_lab(dp)
info_about_creaters.register_handlers_informations(dp)
back_to_menu.register_handlers_back_to_menu(dp)
coming_soon.register_handlers_coming_soon(dp)
how_to_used.register_handler_how_to_used_bot(dp)
feedback.register_message_handler_feedback(dp)

# ------------------------------Orders-------------------------------------- #

create_order_programming.register_handlers_programming(dp)
create_order_math.register_handlers_math(dp)
create_order_it.register_handlers_create_it(dp)
create_order_english.register_message_handler_create_order_english(dp)
application_akj.register_message_handler_get_applications(dp)

# ------------------------------Admins handlers-------------------------------------- #

test_func.register_handlers_test(dp)
notification_all.register_handlers_rozsilaca_messages(dp)
random_choice.register_handlers_choice_winner(dp)


# -------------------------------------------------------------------- #

async def on_start_bot(disp: Dispatcher):
    try:
        await disp.bot.send_message(OWNER, 'Bot started!')
        await set_commands(bot)
    except Exception as e:
        logging.exception(e)


async def set_commands(bt: Bot):
    await bt.set_my_commands([
        types.BotCommand(command='/start', description='Старт'),
        types.BotCommand(command='/back', description='Повернутись в головне меню'),
        types.BotCommand(command='/feedback', description='Відправити нам Ваш Feedback ^^')
    ])


if __name__ == '__main__':
    db.init(os.getenv('DATABASE_DB'))
    db.connect()
    db.create_tables(__all__)
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_bot)
