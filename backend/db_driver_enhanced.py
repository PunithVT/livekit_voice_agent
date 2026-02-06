"""
Enhanced database driver with PostgreSQL support and conversation history
"""
import os
import sqlite3
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from datetime import datetime
import json

# Try to import PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


@dataclass
class Subtopic:
    id: int
    topic: str
    subtopic: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Conversation:
    id: int
    room_name: str
    user_identity: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Message:
    id: int
    conversation_id: int
    role: str  # 'user', 'assistant', or 'system'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserProfile:
    id: int
    user_identity: str
    display_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EnhancedDatabaseDriver:
    """
    Enhanced database driver supporting both SQLite and PostgreSQL
    with conversation history and analytics.
    """

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database driver.

        Args:
            database_url: Database connection string.
                         For SQLite: "sqlite:///path/to/db.sqlite" or just "path/to/db.sqlite"
                         For PostgreSQL: "postgresql://user:pass@host:port/dbname"
        """
        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "tutor_db.sqlite")

        self.database_url = database_url
        self.db_type = self._detect_db_type(database_url)

        if self.db_type == "postgres" and not POSTGRES_AVAILABLE:
            raise RuntimeError("psycopg2 not installed. Install with: pip install psycopg2-binary")

        self._init_db()

    def _detect_db_type(self, url: str) -> str:
        """Detect database type from connection string"""
        if url.startswith("postgresql://") or url.startswith("postgres://"):
            return "postgres"
        return "sqlite"

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager"""
        if self.db_type == "postgres":
            conn = psycopg2.connect(self.database_url)
            conn.autocommit = False
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
        else:
            # SQLite
            db_path = self.database_url.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            finally:
                conn.close()

    def _init_db(self):
        """Initialize database schema"""
        if self.db_type == "sqlite":
            self._init_sqlite()
        else:
            self._init_postgres()

    def _init_sqlite(self):
        """Initialize SQLite schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Subtopics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subtopics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    subtopic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT NOT NULL,
                    user_identity TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    metadata TEXT
                )
            """)

            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            """)

            # User profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_identity TEXT UNIQUE NOT NULL,
                    display_name TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_subtopics_topic ON subtopics(topic)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_room ON conversations(room_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)")

            conn.commit()

    def _init_postgres(self):
        """Initialize PostgreSQL schema"""
        # For PostgreSQL, we rely on the init_db.sql file
        # This method just validates the connection
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")

    # Subtopic methods
    def create_subtopic(self, topic: str, subtopic: str, content: str) -> Subtopic:
        """Create a new subtopic"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO subtopics (topic, subtopic, content)
                    VALUES (%s, %s, %s)
                    RETURNING id, topic, subtopic, content, created_at, updated_at
                    """,
                    (topic, subtopic, content)
                )
                row = cursor.fetchone()
                return Subtopic(*row)
            else:
                cursor.execute(
                    "INSERT INTO subtopics (topic, subtopic, content) VALUES (?, ?, ?)",
                    (topic, subtopic, content)
                )
                sub_id = cursor.lastrowid
                return Subtopic(id=sub_id, topic=topic, subtopic=subtopic, content=content)

    def get_subtopic(self, sub_id: int) -> Optional[Subtopic]:
        """Get subtopic by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            param = "%s" if self.db_type == "postgres" else "?"

            cursor.execute(
                f"SELECT id, topic, subtopic, content, created_at, updated_at FROM subtopics WHERE id = {param}",
                (sub_id,)
            )
            row = cursor.fetchone()
            return Subtopic(*row) if row else None

    def list_subtopics(self, topic: str) -> List[Subtopic]:
        """List all subtopics for a topic"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            param = "%s" if self.db_type == "postgres" else "?"

            cursor.execute(
                f"SELECT id, topic, subtopic, content, created_at, updated_at FROM subtopics WHERE topic = {param}",
                (topic,)
            )
            rows = cursor.fetchall()
            return [Subtopic(*row) for row in rows]

    # Conversation methods
    def create_conversation(self, room_name: str, user_identity: str, metadata: Optional[Dict] = None) -> Conversation:
        """Create a new conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            metadata_str = json.dumps(metadata) if metadata else None

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO conversations (room_name, user_identity, metadata)
                    VALUES (%s, %s, %s::jsonb)
                    RETURNING id, room_name, user_identity, started_at, ended_at, status, metadata
                    """,
                    (room_name, user_identity, metadata_str)
                )
                row = cursor.fetchone()
                return Conversation(*row)
            else:
                cursor.execute(
                    "INSERT INTO conversations (room_name, user_identity, metadata) VALUES (?, ?, ?)",
                    (room_name, user_identity, metadata_str)
                )
                conv_id = cursor.lastrowid
                return Conversation(
                    id=conv_id,
                    room_name=room_name,
                    user_identity=user_identity,
                    started_at=datetime.utcnow(),
                    metadata=metadata
                )

    def add_message(self, conversation_id: int, role: str, content: str, metadata: Optional[Dict] = None) -> Message:
        """Add a message to a conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            metadata_str = json.dumps(metadata) if metadata else None

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO messages (conversation_id, role, content, metadata)
                    VALUES (%s, %s, %s, %s::jsonb)
                    RETURNING id, conversation_id, role, content, timestamp, metadata
                    """,
                    (conversation_id, role, content, metadata_str)
                )
                row = cursor.fetchone()
                return Message(*row)
            else:
                cursor.execute(
                    "INSERT INTO messages (conversation_id, role, content, metadata) VALUES (?, ?, ?, ?)",
                    (conversation_id, role, content, metadata_str)
                )
                msg_id = cursor.lastrowid
                return Message(
                    id=msg_id,
                    conversation_id=conversation_id,
                    role=role,
                    content=content,
                    timestamp=datetime.utcnow(),
                    metadata=metadata
                )

    def get_conversation_messages(self, conversation_id: int, limit: int = 100) -> List[Message]:
        """Get messages from a conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            param = "%s" if self.db_type == "postgres" else "?"

            cursor.execute(
                f"""
                SELECT id, conversation_id, role, content, timestamp, metadata
                FROM messages
                WHERE conversation_id = {param}
                ORDER BY timestamp ASC
                LIMIT {limit}
                """,
                (conversation_id,)
            )
            rows = cursor.fetchall()
            return [Message(*row) for row in rows]

    def end_conversation(self, conversation_id: int):
        """Mark a conversation as ended"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            param = "%s" if self.db_type == "postgres" else "?"

            cursor.execute(
                f"UPDATE conversations SET ended_at = CURRENT_TIMESTAMP, status = 'ended' WHERE id = {param}",
                (conversation_id,)
            )

    # User profile methods
    def create_or_update_user_profile(
        self,
        user_identity: str,
        display_name: Optional[str] = None,
        preferences: Optional[Dict] = None
    ) -> UserProfile:
        """Create or update user profile"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            prefs_str = json.dumps(preferences) if preferences else None

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO user_profiles (user_identity, display_name, preferences)
                    VALUES (%s, %s, %s::jsonb)
                    ON CONFLICT (user_identity)
                    DO UPDATE SET
                        display_name = EXCLUDED.display_name,
                        preferences = EXCLUDED.preferences,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING id, user_identity, display_name, preferences, created_at, updated_at
                    """,
                    (user_identity, display_name, prefs_str)
                )
                row = cursor.fetchone()
                return UserProfile(*row)
            else:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO user_profiles (user_identity, display_name, preferences)
                    VALUES (?, ?, ?)
                    """,
                    (user_identity, display_name, prefs_str)
                )
                return self.get_user_profile(user_identity)

    def get_user_profile(self, user_identity: str) -> Optional[UserProfile]:
        """Get user profile"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            param = "%s" if self.db_type == "postgres" else "?"

            cursor.execute(
                f"""
                SELECT id, user_identity, display_name, preferences, created_at, updated_at
                FROM user_profiles
                WHERE user_identity = {param}
                """,
                (user_identity,)
            )
            row = cursor.fetchone()
            return UserProfile(*row) if row else None


# Singleton instance for backward compatibility
DB = EnhancedDatabaseDriver()
