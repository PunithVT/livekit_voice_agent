"""
WebSocket manager for real-time updates and notifications
"""
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""

    def __init__(self):
        # Active connections by room
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # User identity mapping
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_name: str, user_identity: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()

        # Add to room connections
        if room_name not in self.active_connections:
            self.active_connections[room_name] = set()
        self.active_connections[room_name].add(websocket)

        # Map user to connection
        self.user_connections[user_identity] = websocket

        logger.info(f"WebSocket connected: {user_identity} in room {room_name}")

        # Send welcome message
        await self.send_personal_message(
            {
                "type": "connection",
                "status": "connected",
                "room": room_name,
                "timestamp": datetime.utcnow().isoformat()
            },
            websocket
        )

    def disconnect(self, websocket: WebSocket, room_name: str, user_identity: str):
        """Remove a WebSocket connection"""
        # Remove from room
        if room_name in self.active_connections:
            self.active_connections[room_name].discard(websocket)
            if not self.active_connections[room_name]:
                del self.active_connections[room_name]

        # Remove user mapping
        if user_identity in self.user_connections:
            del self.user_connections[user_identity]

        logger.info(f"WebSocket disconnected: {user_identity} from room {room_name}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def send_to_user(self, user_identity: str, message: dict):
        """Send a message to a specific user"""
        if user_identity in self.user_connections:
            await self.send_personal_message(message, self.user_connections[user_identity])

    async def broadcast_to_room(self, room_name: str, message: dict, exclude: WebSocket = None):
        """Broadcast a message to all connections in a room"""
        if room_name not in self.active_connections:
            return

        disconnected = set()

        for connection in self.active_connections[room_name]:
            if connection == exclude:
                continue

            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to room: {e}")
                disconnected.add(connection)

        # Clean up disconnected connections
        self.active_connections[room_name] -= disconnected

    async def broadcast_all(self, message: dict):
        """Broadcast a message to all connected clients"""
        for room_connections in self.active_connections.values():
            for connection in room_connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error in broadcast all: {e}")

    def get_room_participants(self, room_name: str) -> int:
        """Get the number of participants in a room"""
        if room_name not in self.active_connections:
            return 0
        return len(self.active_connections[room_name])

    def get_all_rooms(self) -> list:
        """Get list of all active rooms"""
        return list(self.active_connections.keys())


# Singleton instance
manager = ConnectionManager()


class EventTypes:
    """WebSocket event type constants"""
    CONNECTION = "connection"
    DISCONNECT = "disconnect"
    MESSAGE = "message"
    TRANSCRIPTION = "transcription"
    AGENT_RESPONSE = "agent_response"
    ROOM_UPDATE = "room_update"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


async def handle_websocket_message(data: dict, websocket: WebSocket, room_name: str):
    """Handle incoming WebSocket messages"""
    message_type = data.get("type")

    if message_type == EventTypes.PING:
        # Respond to ping with pong
        await manager.send_personal_message(
            {"type": EventTypes.PONG, "timestamp": datetime.utcnow().isoformat()},
            websocket
        )

    elif message_type == EventTypes.MESSAGE:
        # Broadcast user message to room
        await manager.broadcast_to_room(
            room_name,
            {
                "type": EventTypes.MESSAGE,
                "user": data.get("user"),
                "content": data.get("content"),
                "timestamp": datetime.utcnow().isoformat()
            },
            exclude=websocket
        )

    else:
        logger.warning(f"Unknown message type: {message_type}")
