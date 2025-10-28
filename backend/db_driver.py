import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Subtopic:
    id: int
    topic: str
    subtopic: str
    content: str

class DatabaseDriver:
    """Simple SQLite driver for storing tutoring subtopics and conversation history."""
    def __init__(self, db_path: str = "tutor_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS subtopics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    subtopic TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_subtopic(self, topic: str, subtopic: str, content: str) -> Subtopic:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO subtopics (topic, subtopic, content) VALUES (?, ?, ?)",
                (topic, subtopic, content)
            )
            conn.commit()
            sub_id = cursor.lastrowid
            return Subtopic(id=sub_id, topic=topic, subtopic=subtopic, content=content)

    def get_subtopic(self, sub_id: int) -> Optional[Subtopic]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, topic, subtopic, content FROM subtopics WHERE id = ?",
                (sub_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Subtopic(id=row[0], topic=row[1], subtopic=row[2], content=row[3])

    def list_subtopics(self, topic: str) -> List[Subtopic]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, topic, subtopic, content FROM subtopics WHERE topic = ?",
                (topic,)
            )
            rows = cursor.fetchall()
            return [Subtopic(id=r[0], topic=r[1], subtopic=r[2], content=r[3]) for r in rows]
