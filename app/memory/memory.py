import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "nova_memory.db"


class Memory:

    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.create_table()

    # ============================================================
    # DATABASE SETUP + MIGRATION
    # ============================================================

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                importance INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        columns = self.connection.execute(
            "PRAGMA table_info(memories)"
        ).fetchall()

        existing_columns = {
            column["name"]
            for column in columns
        }

        # Add category to old databases
        if "category" not in existing_columns:
            self.connection.execute("""
                ALTER TABLE memories
                ADD COLUMN category TEXT DEFAULT 'general'
            """)

        # Add importance to old databases
        if "importance" not in existing_columns:
            self.connection.execute("""
                ALTER TABLE memories
                ADD COLUMN importance INTEGER DEFAULT 1
            """)

        # Add updated_at safely to old databases
        if "updated_at" not in existing_columns:
            self.connection.execute("""
                ALTER TABLE memories
                ADD COLUMN updated_at TIMESTAMP
            """)

            # Populate updated_at for existing memories
            self.connection.execute("""
                UPDATE memories
                SET updated_at = created_at
                WHERE updated_at IS NULL
            """)

        # Make sure any NULL values are populated
        self.connection.execute("""
            UPDATE memories
            SET updated_at = created_at
            WHERE updated_at IS NULL
        """)

        # ========================================================
        # INDEXES
        # ========================================================

        self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_key
            ON memories(key)
        """)

        self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_category
            ON memories(category)
        """)

        self.connection.commit()

    # ============================================================
    # REMEMBER
    # ============================================================

    def remember(
        self,
        key,
        value,
        category="general",
        importance=1
    ):
        existing = self.connection.execute(
            """
            SELECT id
            FROM memories
            WHERE key = ?
            AND value = ?
            LIMIT 1
            """,
            (key, value)
        ).fetchone()

        if existing:
            return existing["id"]

        cursor = self.connection.execute(
            """
            INSERT INTO memories (
                key,
                value,
                category,
                importance,
                updated_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                key,
                value,
                category,
                importance
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    # ============================================================
    # RECALL
    # ============================================================

    def recall(self, key):
        result = self.connection.execute(
            """
            SELECT value
            FROM memories
            WHERE key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (key,)
        ).fetchone()

        if result:
            return result["value"]

        return None

    # ============================================================
    # SEARCH
    # ============================================================

    def search(self, query, limit=10):
        search_term = f"%{query}%"

        cursor = self.connection.execute(
            """
            SELECT
                id,
                key,
                value,
                category,
                importance,
                created_at,
                updated_at
            FROM memories
            WHERE key LIKE ?
               OR value LIKE ?
               OR category LIKE ?
            ORDER BY
                importance DESC,
                id DESC
            LIMIT ?
            """,
            (
                search_term,
                search_term,
                search_term,
                limit
            )
        )

        return cursor.fetchall()

    # ============================================================
    # GET ALL
    # ============================================================

    def get_all(self):
        cursor = self.connection.execute(
            """
            SELECT
                id,
                key,
                value,
                category,
                importance,
                created_at,
                updated_at
            FROM memories
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    # ============================================================
    # GET IMPORTANT MEMORIES
    # ============================================================

    def get_important(self, limit=10):
        cursor = self.connection.execute(
            """
            SELECT
                id,
                key,
                value,
                category,
                importance,
                created_at,
                updated_at
            FROM memories
            WHERE importance >= 2
            ORDER BY importance DESC, id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    # ============================================================
    # DELETE MEMORY BY ID
    # ============================================================

    def delete(self, memory_id):
        cursor = self.connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,)
        )

        self.connection.commit()

        return cursor.rowcount > 0

    # ============================================================
    # FORGET BY KEY
    # ============================================================

    def forget(self, key):
        cursor = self.connection.execute(
            """
            DELETE FROM memories
            WHERE key = ?
            """,
            (key,)
        )

        self.connection.commit()

        return cursor.rowcount

    # ============================================================
    # CLEAR ALL MEMORIES
    # ============================================================

    def clear(self):
        self.connection.execute(
            "DELETE FROM memories"
        )

        self.connection.commit()

    # ============================================================
    # CLOSE DATABASE
    # ============================================================

    def close(self):
        self.connection.close()