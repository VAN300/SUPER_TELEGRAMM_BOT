import os
from io import BytesIO
from pathlib import Path
from threading import Thread

from aiogram import executor
from aiogram import types

from Singleton import singleton
from utils import add_watermark

SAVE_DIR = Path(os.getcwd(), "cache")


@singleton.dispatcher.message_handler(commands=["start", "help", "помощь"])
async def hello(message):
    await message.reply(
        """
        Использование:
        1) Установите текст командоq
           /set Какой-то текст
        2) Отправьте изображение
        3) Готово
        """
    )


@singleton.dispatcher.message_handler(content_types=["photo", "document"])
async def image(message: types.Message):
    """
    Загружать ВСЕ картинки
    """

    await message.reply("Работаем!")
    buffer = BytesIO()
    if message.photo:
        await message.photo[-1].download(destination_file=buffer)
    else:
        await message.document.download(destination_file=buffer)

    Thread(target=add_watermark, daemon=True, args=(buffer, message.chat.id)).start()


@singleton.dispatcher.message_handler(commands=["set", "установить"])
async def set_watermark(message: types.Message):
    if message.get_args().strip() != "":
        singleton.table.set_watermark(message.chat.id, message.get_args())
        await message.reply("Был установлен текст водного знака: " + singleton.table.get_watermark(message.chat.id))
    else:
        await message.reply("Использование /set ТЕКСТ")


def main():
    executor.start_polling(dispatcher=singleton.dispatcher, skip_updates=True)


if __name__ == "__main__":
    main()
