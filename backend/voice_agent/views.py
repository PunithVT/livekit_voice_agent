import os
from livekit import api
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid
import asyncio

load_dotenv()

async def generate_room_name():
    """Generate a unique room name."""
    name = "room-" + str(uuid.uuid4())[:8]
    rooms = await get_rooms()
    while name in rooms:
        name = "room-" + str(uuid.uuid4())[:8]
    return name

async def get_rooms():
    """Get list of active rooms."""
    lk_api = LiveKitAPI()
    rooms = await lk_api.room.list_rooms(ListRoomsRequest())
    await lk_api.aclose()
    return [room.name for room in rooms.rooms]

@csrf_exempt
@require_http_methods(["GET"])
async def get_token(request):
    """Generate a LiveKit token for joining a voice session."""
    try:
        name = request.GET.get("name", "Student")
        room = request.GET.get("room", None)
        
        if not room:
            room = await generate_room_name()
        
        # Get LiveKit credentials from environment
        livekit_api_key = os.getenv("LIVEKIT_API_KEY")
        livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")
        
        if not livekit_api_key or not livekit_api_secret:
            return JsonResponse({
                'error': 'LiveKit credentials not configured'
            }, status=500)
        
        # Generate access token
        token = api.AccessToken(livekit_api_key, livekit_api_secret) \
            .with_identity(name) \
            .with_name(name) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room
            ))
        
        return JsonResponse({
            'token': token.to_jwt(),
            'room': room,
            'url': os.getenv("LIVEKIT_URL")
        })
    
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_config(request):
    """Get voice agent configuration."""
    try:
        return JsonResponse({
            'livekit_url': os.getenv("LIVEKIT_URL"),
            'topic': os.getenv("TUTOR_TOPIC", "artificial intelligence"),
            'subject': os.getenv("TUTOR_SUBJECT", "machine learning basics"),
            'style': os.getenv("TUTOR_STYLE", "friendly and encouraging")
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
