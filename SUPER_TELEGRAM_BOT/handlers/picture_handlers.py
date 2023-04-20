import asyncio
from io import BytesIO
from threading import Thread

from aiogram import types, Bot, Dispatcher
from singleton import Singleton
from utils import *

singleton = Singleton()
dp: Dispatcher = singleton.dispatcher
bot: Bot = singleton.bot


@dp.message_handler(content_types=["photo"])
async def quallity_upgrade(message: types.Message):
    buffer: BytesIO = BytesIO()

    await message.photo[-1].download(destination_file=buffer)
    await message.answer("Обработка...")

    thread = Thread(target=upgrade, args=(buffer, message))
    thread.start()


@dp.message_handler(content_types=["document"])
async def quallity_upgrade(message: types.Message):
    buffer: BytesIO = BytesIO()

    await message.document.download(buffer)
    await message.answer("Обработка...")

    thread = Thread(target=upgrade, args=(buffer, message))
    thread.start()


print("Обработчики изображений зарегистрированы!")
