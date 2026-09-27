import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "nova_memory.db"


class Memory:
    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def remember(self, key, value):
        self.connection.execute(
            """
            INSERT INTO memories (key, value)
            VALUES (?, ?)
            """,
            (key, value)
        )

        self.connection.commit()

    def recall(self, key):
        cursor = self.connection.execute(
            """
            SELECT value
            FROM memories
            WHERE key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (key,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    def get_all(self):
        cursor = self.connection.execute(
            """
            SELECT key, value, created_at
            FROM memories
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    def close(self):
        self.connection.close()
        