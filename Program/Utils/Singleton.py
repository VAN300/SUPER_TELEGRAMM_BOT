import asyncio

from aiogram import Bot, Dispatcher

from Program.Bases import WatermarkTable


class Singleton:
    _instance = None

    def __init__(self):
        self.bot: Bot = Bot(token="token")
        self.dispatcher: Dispatcher = Dispatcher(self.bot, loop=asyncio.get_event_loop())
        self.table: WatermarkTable = WatermarkTable()

    def __new__(cls):
        if getattr(cls, '_instance') is None:
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance


singleton: Singleton = Singleton()
