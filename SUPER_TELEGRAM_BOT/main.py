#!/usr/bin/env python
from aiogram import executor
from dotenv import load_dotenv


def main():
    load_dotenv()
    import handlers

    executor.start_polling(handlers.dp, skip_updates=True)


if __name__ == "__main__":
    main()
