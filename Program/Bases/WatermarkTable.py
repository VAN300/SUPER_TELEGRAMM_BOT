import os
import sqlite3
from pathlib import Path


class WatermarkTable:
    TABLE = Path(os.getcwd(), "base.db")

    def __init__(self):
        self.connection = sqlite3.connect(WatermarkTable.TABLE, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.prepare()

    def prepare(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS watermarks(
                chatId INT PRIMARY KEY,
                watermark TEXT
                )
            """
        )
        self.connection.commit()

    def get_watermark(self, chat_id):
        self.cursor.execute(
            """
            SELECT *
            FROM watermarks
            
            WHERE chatId = ?
            """, (str(chat_id),)
        )

        result = self.cursor.fetchone()

        if result:
            return result[1]
        return "Установите текст"

    def set_watermark(self, chat_id, watermark: str):
        exists = self.cursor.execute(
            """
            SELECT * 
            FROM watermarks
            WHERE chatId == ?
            """, (chat_id,)
        ).fetchone()

        if not exists:
            self.__paste(chat_id, watermark)

        self.cursor.execute(
            """
            UPDATE watermarks
            
            SET watermark = ?
            
            WHERE chatId == ?
            """, (watermark, str(chat_id))
        )
        self.connection.commit()

    def __paste(self, chat_id, watermark):
        self.cursor.execute(
            """
            INSERT INTO watermarks
            (chatId, watermark)
            VALUES
            (?, ?)
            """, (chat_id, watermark)
        )
        self.connection.commit()

    def get_count(self):
        results = self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM watermarks
            """
        ).fetchone()
        return results[0]
