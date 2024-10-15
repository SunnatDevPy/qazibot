import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bot.handlers import private_handler_router
from config import conf
from db import database


async def on_start(bot: Bot):
    await database.create_all()
    commands_admin = [
        BotCommand(command='start', description="Bo'tni ishga tushirish"),
    ]
    await bot.set_my_commands(commands=commands_admin)
    text = '«Qazi» rasmiy sotuv boti'
    await bot.set_my_description(text, 'uz')


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main():
    dp = Dispatcher()
    dp.include_routers(private_handler_router)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=conf.bot.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# 1065  docker login
# 1068  docker build -t nickname/name .
# 1071  docker push nickname/name

# docker run --name db_mysql -e MYSQL_ROOT_PASSWORD=1 -d mysql
