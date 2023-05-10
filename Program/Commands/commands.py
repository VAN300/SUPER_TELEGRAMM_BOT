import os
from io import BytesIO
from pathlib import Path
from threading import Thread

from Program.Buttons import *
from Program.Handlers import add_watermark
from Program.Utils import singleton

SAVE_DIR = Path(os.getcwd(), "cache")
ASSET = Path(os.getcwd(), "assets", "help.png")


@singleton.dispatcher.message_handler(commands=["start"])
async def start(message):
    await message.answer("Используйте кнопки.", reply_markup=START)


@singleton.dispatcher.message_handler(text=HELP)
async def help_bot(message):
    await message.answer(
        """
        Использование:
        help.png) Установите текст командой
           /set Какой-то текст
        2) Отправьте изображение
        3) Готово
        """
    )
    await singleton.bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(ASSET))


@singleton.dispatcher.message_handler(content_types=["photo", "document"])
async def image(message: types.Message):
    await message.reply("Обработка...")
    buffer = BytesIO()

    if message.photo:
        await message.photo[-1].download(destination_file=buffer)
    else:
        await message.document.download(destination_file=buffer)

    Thread(target=add_watermark, daemon=True, args=(buffer, message.chat.id)).start()


@singleton.dispatcher.message_handler(commands=["set"])
async def set_watermark(message: types.Message):
    singleton.table.set_watermark(message.chat.id, message.get_args())
    await message.answer("Был установлен текст водяного знака: " + singleton.table.get_watermark(message.chat.id))


@singleton.dispatcher.message_handler(text=USERS)
async def users(message: types.Message):
    await message.reply(singleton.table.get_count())
