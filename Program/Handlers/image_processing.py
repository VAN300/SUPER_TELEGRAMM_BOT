import os
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFont, ImageDraw
from aiogram import types

from Program.Utils import singleton

FONT = Path(os.getcwd(), "Fonts/" "arial.ttf")


def add_watermark(buffer: BytesIO, id):
    text = singleton.table.get_watermark(id)
    font: ImageFont = ImageFont.truetype(FONT.__str__(), 85)
    image: Image = Image.open(buffer).convert("RGBA")

    text_image: Image = Image.new("RGBA", image.size, (0xFF, 0xFF, 0xFF, 0x00))
    imageDraw: ImageDraw = ImageDraw.Draw(text_image)

    width, height = image.size
    text_w, text_h = imageDraw.textsize(text, font)

    size = (width - text_w) / 2, (height - text_h) / 2
    imageDraw.text(size, text, fill=(0xFF, 0xFF, 0xFF, 0x90), font=font)
    text_image = text_image.rotate(30)
    watermark = Image.alpha_composite(image, text_image)

    result = BytesIO()
    watermark.save(result, "PNG")
    result.seek(0)

    singleton.dispatcher.loop.create_task(
        singleton.bot.send_document(id, types.InputFile(result, filename="Result.png"), caption="Результат")
    )
