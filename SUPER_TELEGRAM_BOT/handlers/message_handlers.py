from aiogram import types

from singleton import Singleton

dp = Singleton().dispatcher


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Этот обработчик будет вызван после ввода команды /start или /help
    """
    await message.answer("Nothing")


@dp.message_handler()
async def echo(message: types.Message):
    """
    Функция инвертирующая сообщение и отправляющая его обратнояё
    """
    await message.answer(message.text[::-1])


print("Обработчики сообщений зарегистрированы!")
