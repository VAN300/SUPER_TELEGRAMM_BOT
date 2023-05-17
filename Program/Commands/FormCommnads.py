from aiogram import types

from Program.Buttons import SET
from Program.Utils import Form
from Program.Utils import singleton


@singleton.dispatcher.message_handler(text=SET)
async def form(message: types.Message):
    await message.answer("Введите текст водяного знака")
    await Form.text.set()


@singleton.dispatcher.message_handler(state=Form.text)
async def name(message: types.Message, state):
    async with state.proxy() as data:
        data['text'] = message.text

    await message.answer("Введите угол наклона водяного знака в градусах")
    await Form.next()


@singleton.dispatcher.message_handler(state=Form.angel)
async def angel(message: types.Message, state):
    async with state.proxy() as data:
        try:
            message.text = int(message.text)
        except Exception as exc:
            message.text = 0

        data['angel'] = message.text

    singleton.table.set_watermark(message.chat.id,
                                  data['text'],
                                  data['angel']
                                  )
    await message.answer(f"Установлено"
                         f"\nТекст водяного знака: {data['text']}"
                         f" \nТекст угол наклона: {data['angel']}")

    await state.finish()


print("Подключено", __name__)
