from aiogram import types

HELP = "Инструкция по использованию"
SET = "Установить текст водяного знака"
USERS = "Количество пользователей"

START = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
START.add(types.InlineKeyboardButton(HELP))
START.add(types.InlineKeyboardButton(USERS))
