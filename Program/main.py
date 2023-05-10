from aiogram import executor

from Commands import *


def main():
    executor.start_polling(dispatcher=singleton.dispatcher, skip_updates=True)


if __name__ == "__main__":
    main()
