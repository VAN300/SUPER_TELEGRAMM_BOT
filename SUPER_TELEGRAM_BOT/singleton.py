import asyncio
import os
from pathlib import Path

import tensorflow
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

PATH = Path("models/esrgan-tf2_1")


class Singleton:
    _instance = None

    def __new__(cls):
        if getattr(cls, '_instance') is None:
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance


loop = asyncio.get_event_loop()
singleton = Singleton()

singleton.bot: Bot = Bot(token=os.getenv("API_TOKEN"))
singleton.storage: MemoryStorage = MemoryStorage()
singleton.dispatcher: Dispatcher = Dispatcher(singleton.bot, storage=singleton.storage, loop=loop)
singleton.model = tensorflow.saved_model.load(PATH)
