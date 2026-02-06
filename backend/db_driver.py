import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime
import json

@dataclass
class Subtopic:
    id: int
    topic: str
    subtopic: str
    content: str

@dataclass
class Conversation:
    id: int
    room_name: str
    user_identity: str
    started_at: str
    ended_at: Optional[str] = None
    status: str = "active"

@dataclass
class Message:
    id: int
    conversation_id: int
    role: str  # 'user', 'assistant', or 'system'
    content: str
    timestamp: str

class DatabaseDriver:
    """SQLite driver for storing tutoring subtopics and conversation history."""
    def __init__(self, db_path: str = "tutor_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Subtopics table
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

            # Conversations table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT NOT NULL,
                    user_identity TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
                """
            )

            # Messages table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
                """
            )

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_subtopics_topic ON subtopics(topic)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_room ON conversations(room_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)")

            conn.commit()

    # Subtopic methods
    def create_subtopic(self, topic: str, subtopic: str, content: str) -> Subtopic:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO subtopics (topic, subtopic, content) VALUES (?, ?, ?)",
                (topic, subtopic, content)
            )
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

    # Conversation methods
    def create_conversation(self, room_name: str, user_identity: str) -> Conversation:
        """Create a new conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (room_name, user_identity) VALUES (?, ?)",
                (room_name, user_identity)
            )
            conv_id = cursor.lastrowid
            cursor.execute(
                "SELECT id, room_name, user_identity, started_at, ended_at, status FROM conversations WHERE id = ?",
                (conv_id,)
            )
            row = cursor.fetchone()
            return Conversation(
                id=row[0],
                room_name=row[1],
                user_identity=row[2],
                started_at=row[3],
                ended_at=row[4],
                status=row[5]
            )

    def add_message(self, conversation_id: int, role: str, content: str) -> Message:
        """Add a message to a conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )
            msg_id = cursor.lastrowid
            cursor.execute(
                "SELECT id, conversation_id, role, content, timestamp FROM messages WHERE id = ?",
                (msg_id,)
            )
            row = cursor.fetchone()
            return Message(
                id=row[0],
                conversation_id=row[1],
                role=row[2],
                content=row[3],
                timestamp=row[4]
            )

    def get_conversation_messages(self, conversation_id: int, limit: int = 100) -> List[Message]:
        """Get messages from a conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, conversation_id, role, content, timestamp
                FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
                """,
                (conversation_id, limit)
            )
            rows = cursor.fetchall()
            return [Message(
                id=r[0],
                conversation_id=r[1],
                role=r[2],
                content=r[3],
                timestamp=r[4]
            ) for r in rows]

    def end_conversation(self, conversation_id: int):
        """Mark a conversation as ended"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE conversations SET ended_at = CURRENT_TIMESTAMP, status = 'ended' WHERE id = ?",
                (conversation_id,)
            )

    def get_active_conversation(self, room_name: str) -> Optional[Conversation]:
        """Get active conversation for a room"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, room_name, user_identity, started_at, ended_at, status
                FROM conversations
                WHERE room_name = ? AND status = 'active'
                ORDER BY started_at DESC
                LIMIT 1
                """,
                (room_name,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Conversation(
                id=row[0],
                room_name=row[1],
                user_identity=row[2],
                started_at=row[3],
                ended_at=row[4],
                status=row[5]
            )
