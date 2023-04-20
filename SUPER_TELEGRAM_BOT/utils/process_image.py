from io import BytesIO

import numpy
import tensorflow
from PIL import Image
from aiogram import Bot
from singleton import Singleton

dispatcher = Singleton().dispatcher
bot: Bot = Singleton().bot


def upgrade(data: BytesIO, message):
    hr_image = tensorflow.image.decode_image(data.getvalue())
    image = tensorflow.expand_dims(hr_image, 0)
    image = tensorflow.cast(image, tensorflow.float32)

    best_resolution = Singleton().model(image)

    image = numpy.asarray(best_resolution)
    image = tensorflow.clip_by_value(image, 0, 255)
    image = Image.fromarray(tensorflow.cast(image[0], tensorflow.uint8).numpy())

    output = BytesIO()
    image.save(output, "JPEG")

    dispatcher.loop.create_task(
        bot.send_photo(chat_id=message.chat.id, photo=output.getvalue())
    )
    dispatcher.loop.create_task(
        message.answer("Оно не работает! ЧОРТ!")
    )
