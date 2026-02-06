"""
FastAPI server for LiveKit Voice Agent
Provides token generation, room management, and API endpoints
"""
import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends, Query, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from livekit import api
from livekit.api import LiveKitAPI, ListRoomsRequest
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from websocket_manager import manager, EventTypes, handle_websocket_message

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LiveKit Voice Agent API",
    description="Real-time voice tutoring platform with AI-powered agents",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Prometheus metrics
token_requests = Counter('token_requests_total', 'Total token requests')
token_errors = Counter('token_errors_total', 'Total token generation errors')
room_creations = Counter('room_creations_total', 'Total room creations')
api_latency = Histogram('api_request_duration_seconds', 'API request latency')

# Pydantic Models
class TokenRequest(BaseModel):
    """Request model for token generation"""
    name: str = Field(..., min_length=1, max_length=100, description="User's display name")
    room: Optional[str] = Field(None, max_length=100, description="Specific room name to join")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional user metadata")

class TokenResponse(BaseModel):
    """Response model for token generation"""
    token: str = Field(..., description="JWT access token for LiveKit")
    room: str = Field(..., description="Room name")
    url: str = Field(..., description="LiveKit server URL")
    identity: str = Field(..., description="User identity")
    expires_at: datetime = Field(..., description="Token expiration time")

class RoomInfo(BaseModel):
    """Room information model"""
    name: str
    num_participants: int
    creation_time: datetime
    metadata: Optional[dict] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    livekit_connected: bool

# Helper functions
async def generate_room_name() -> str:
    """Generate a unique room name"""
    name = f"room-{uuid.uuid4().hex[:8]}"
    rooms = await get_rooms()

    while name in [room.name for room in rooms]:
        name = f"room-{uuid.uuid4().hex[:8]}"

    room_creations.inc()
    logger.info(f"Generated new room name: {name}")
    return name

async def get_rooms() -> List[RoomInfo]:
    """Get list of active rooms from LiveKit"""
    try:
        lk_api = LiveKitAPI()
        rooms_response = await lk_api.room.list_rooms(ListRoomsRequest())
        await lk_api.aclose()

        return [
            RoomInfo(
                name=room.name,
                num_participants=room.num_participants,
                creation_time=datetime.fromtimestamp(room.creation_time),
                metadata={"sid": room.sid}
            )
            for room in rooms_response.rooms
        ]
    except Exception as e:
        logger.error(f"Error fetching rooms: {str(e)}")
        return []

def validate_env_vars():
    """Validate required environment variables"""
    required_vars = ["LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    try:
        validate_env_vars()
        logger.info("FastAPI server started successfully")
        logger.info(f"LiveKit URL: {os.getenv('LIVEKIT_URL', 'Not configured')}")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "LiveKit Voice Agent API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    livekit_connected = True
    try:
        await get_rooms()
    except Exception as e:
        logger.warning(f"LiveKit health check failed: {str(e)}")
        livekit_connected = False

    return HealthResponse(
        status="healthy" if livekit_connected else "degraded",
        timestamp=datetime.utcnow(),
        version="2.0.0",
        livekit_connected=livekit_connected
    )

@app.get("/api/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/api/getToken", response_model=TokenResponse, tags=["Authentication"])
@limiter.limit("10/minute")
async def get_token_legacy(
    request: __import__('fastapi').Request,
    name: str = Query("Guest", description="User's display name"),
    room: Optional[str] = Query(None, description="Room name to join")
):
    """
    Legacy endpoint for backward compatibility.
    Generate a JWT token for LiveKit room access.
    """
    token_requests.inc()

    try:
        # Generate room name if not provided
        if not room:
            room = await generate_room_name()

        # Validate environment
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")
        livekit_url = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

        if not api_key or not api_secret:
            token_errors.inc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LiveKit credentials not configured"
            )

        # Create access token
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(name) \
            .with_name(name) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True
            )) \
            .with_ttl(timedelta(hours=2))

        jwt_token = token.to_jwt()

        logger.info(f"Token generated for user '{name}' in room '{room}'")

        return TokenResponse(
            token=jwt_token,
            room=room,
            url=livekit_url,
            identity=name,
            expires_at=datetime.utcnow() + timedelta(hours=2)
        )

    except Exception as e:
        token_errors.inc()
        logger.error(f"Token generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate token: {str(e)}"
        )

@app.post("/api/token", response_model=TokenResponse, tags=["Authentication"])
@limiter.limit("10/minute")
async def create_token(
    request: __import__('fastapi').Request,
    token_request: TokenRequest
):
    """
    Generate a JWT token for LiveKit room access.
    Supports custom metadata and room specification.
    """
    token_requests.inc()

    try:
        # Generate room name if not provided
        room = token_request.room or await generate_room_name()

        # Validate environment
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")
        livekit_url = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

        if not api_key or not api_secret:
            token_errors.inc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LiveKit credentials not configured"
            )

        # Create access token with extended permissions
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(token_request.name) \
            .with_name(token_request.name) \
            .with_metadata(str(token_request.metadata)) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True
            )) \
            .with_ttl(timedelta(hours=2))

        jwt_token = token.to_jwt()

        logger.info(f"Token generated for user '{token_request.name}' in room '{room}'")

        return TokenResponse(
            token=jwt_token,
            room=room,
            url=livekit_url,
            identity=token_request.name,
            expires_at=datetime.utcnow() + timedelta(hours=2)
        )

    except Exception as e:
        token_errors.inc()
        logger.error(f"Token generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate token: {str(e)}"
        )

@app.get("/api/rooms", response_model=List[RoomInfo], tags=["Rooms"])
@limiter.limit("20/minute")
async def list_rooms(request: __import__('fastapi').Request):
    """List all active LiveKit rooms"""
    try:
        rooms = await get_rooms()
        logger.info(f"Retrieved {len(rooms)} active rooms")
        return rooms
    except Exception as e:
        logger.error(f"Error listing rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list rooms: {str(e)}"
        )

@app.delete("/api/rooms/{room_name}", tags=["Rooms"])
@limiter.limit("5/minute")
async def delete_room(
    request: __import__('fastapi').Request,
    room_name: str
):
    """Delete a specific room"""
    try:
        lk_api = LiveKitAPI()
        await lk_api.room.delete_room(api.DeleteRoomRequest(room=room_name))
        await lk_api.aclose()

        logger.info(f"Room '{room_name}' deleted successfully")
        return {"message": f"Room '{room_name}' deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete room: {str(e)}"
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# WebSocket endpoints
@app.websocket("/ws/{room_name}/{user_identity}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, user_identity: str):
    """
    WebSocket endpoint for real-time updates.

    Provides real-time notifications for:
    - Room events (user joined/left)
    - Message updates
    - Transcriptions
    - Agent responses
    """
    await manager.connect(websocket, room_name, user_identity)

    try:
        # Notify room about new user
        await manager.broadcast_to_room(
            room_name,
            {
                "type": EventTypes.USER_JOINED,
                "user": user_identity,
                "timestamp": datetime.utcnow().isoformat(),
                "participants": manager.get_room_participants(room_name)
            },
            exclude=websocket
        )

        # Message receive loop
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(data, websocket, room_name)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_name, user_identity)

        # Notify room about user leaving
        await manager.broadcast_to_room(
            room_name,
            {
                "type": EventTypes.USER_LEFT,
                "user": user_identity,
                "timestamp": datetime.utcnow().isoformat(),
                "participants": manager.get_room_participants(room_name)
            }
        )
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, room_name, user_identity)

@app.get("/api/ws/rooms", tags=["WebSocket"])
async def list_websocket_rooms():
    """List all active WebSocket rooms"""
    rooms = manager.get_all_rooms()
    return {
        "rooms": rooms,
        "count": len(rooms),
        "details": [
            {
                "room": room,
                "participants": manager.get_room_participants(room)
            }
            for room in rooms
        ]
    }

# Analytics endpoints
@app.get("/api/analytics/conversations/{conversation_id}", tags=["Analytics"])
async def get_conversation_analytics(conversation_id: int):
    """Get analytics for a specific conversation"""
    try:
        from db_driver import DatabaseDriver
        db = DatabaseDriver()

        messages = db.get_conversation_messages(conversation_id)

        # Calculate metrics
        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        return {
            "conversation_id": conversation_id,
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "message_breakdown": {
                "user": len(user_messages),
                "assistant": len(assistant_messages),
                "system": len([m for m in messages if m.role == "system"])
            }
        }
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )

@app.get("/api/analytics/summary", tags=["Analytics"])
async def get_overall_analytics():
    """Get overall platform analytics"""
    try:
        from db_driver import DatabaseDriver
        import sqlite3

        db = DatabaseDriver()

        with db._get_connection() as conn:
            cursor = conn.cursor()

            # Total conversations
            cursor.execute("SELECT COUNT(*) FROM conversations")
            total_conversations = cursor.fetchone()[0]

            # Active conversations
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE status = 'active'")
            active_conversations = cursor.fetchone()[0]

            # Total messages
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]

            # Total subtopics
            cursor.execute("SELECT COUNT(*) FROM subtopics")
            total_subtopics = cursor.fetchone()[0]

            # Top topics
            cursor.execute("""
                SELECT topic, COUNT(*) as count
                FROM subtopics
                GROUP BY topic
                ORDER BY count DESC
                LIMIT 5
            """)
            top_topics = [{"topic": row[0], "count": row[1]} for row in cursor.fetchall()]

        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_messages": total_messages,
            "total_subtopics": total_subtopics,
            "top_topics": top_topics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Analytics summary error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics summary: {str(e)}"
        )

# Run with uvicorn
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "5001"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("DEBUG", "true").lower() == "true"

    logger.info(f"Starting FastAPI server on {host}:{port}")

    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )
