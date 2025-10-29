# Voice Agent Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          User's Browser                              │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    React Frontend                               │ │
│  │                  (localhost:5173)                               │ │
│  │                                                                 │ │
│  │  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐  │ │
│  │  │ Voice Button │───▶│ Modal Dialog │───▶│ LiveKit Room UI │  │ │
│  │  └──────────────┘    └──────────────┘    └─────────────────┘  │ │
│  │                                                 │               │ │
│  │                                                 │ WebSocket     │ │
│  └─────────────────────────────────────────────────┼───────────────┘ │
│                                                    │                 │
└────────────────────────────────────────────────────┼─────────────────┘
                                                     │
                          ┌──────────────────────────┼─────────┐
                          │                          │         │
                          │                          ▼         │
                    HTTP  │            ┌──────────────────────┐│
                    API   │            │   LiveKit Cloud      ││
                          │            │  (Real-time Audio)   ││
                          │            └──────────────────────┘│
                          │                     │              │
                          ▼                     │ WebSocket    │
         ┌──────────────────────────┐          │              │
         │   Django Backend         │          │              │
         │   (localhost:8000)       │          │              │
         │  ┌────────────────────┐  │          │              │
         │  │  API Endpoints     │  │          │              │
         │  │  /api/voice/       │  │          │              │
         │  │  - get-token/      │  │          │              │
         │  │  - config/         │  │          │              │
         │  └────────────────────┘  │          │              │
         │                          │          │              │
         │  ┌────────────────────┐  │          │              │
         │  │  voice_agent App   │  │          │              │
         │  │  - views.py        │  │          │              │
         │  │  - db_driver.py    │  │          │              │
         │  └────────────────────┘  │          │              │
         └──────────────────────────┘          │              │
                                                │              │
         ┌──────────────────────────────────────┼──────────────┘
         │     LiveKit Agent Process            │
         │     (python agent.py dev)            │
         │                                      │
         │  ┌────────────────────────────────┐ │
         │  │  TutorAgent Class              │ │
         │  │  - Teaching Logic              │ │
         │  │  - Function Tools              │ │
         │  │  - Conversation Flow           │ │
         │  └────────────────────────────────┘ │
         │           │         │         │      │
         └───────────┼─────────┼─────────┼──────┘
                     │         │         │
                     ▼         ▼         ▼
         ┌──────────────┐ ┌──────────┐ ┌─────────────┐
         │  Deepgram    │ │  OpenAI  │ │   SQLite    │
         │  (STT)       │ │  (LLM +  │ │  (History)  │
         │              │ │   TTS)   │ │             │
         └──────────────┘ └──────────┘ └─────────────┘
             Speech           AI           Storage
             Recognition      Response     Database
```

## Component Flow

### 1. Session Initiation
```
User clicks Voice Button
    ↓
Modal opens with name form
    ↓
User enters name and clicks "Start"
    ↓
Frontend requests token from Django API
    ↓
Django generates LiveKit access token
    ↓
Frontend receives token + room info
    ↓
LiveKit Room component connects
```

### 2. Voice Interaction Flow
```
User speaks into microphone
    ↓
Audio sent to LiveKit Cloud via WebSocket
    ↓
LiveKit routes audio to Agent
    ↓
Agent uses Deepgram for Speech-to-Text
    ↓
Text sent to OpenAI LLM for processing
    ↓
Agent uses function tools (check_understanding, etc.)
    ↓
LLM generates response
    ↓
OpenAI TTS converts response to audio
    ↓
Audio sent back through LiveKit
    ↓
User hears response in browser
    ↓
Transcriptions displayed in real-time
```

## Key Technologies

### Frontend Stack
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Styled Components** - Styling
- **Framer Motion** - Animations
- **LiveKit React Components** - Voice UI
  - `useVoiceAssistant` - Agent state management
  - `BarVisualizer` - Audio visualization
  - `VoiceAssistantControlBar` - Controls
  - `useTrackTranscription` - Real-time transcription

### Backend Stack
- **Django 4.2+** - Web framework
- **Django REST Framework** - API
- **LiveKit Python SDK** - Agent framework
- **LiveKit API** - Token generation

### AI Services
- **LiveKit Cloud** - Real-time communication
- **Deepgram Nova-2** - Speech-to-Text
- **OpenAI GPT-4** - Language model
- **OpenAI TTS** - Text-to-Speech
- **Silero VAD** - Voice Activity Detection

## Data Flow Details

### Token Generation Flow
```python
# 1. Frontend Request
GET /api/voice/get-token/?name=Alice

# 2. Django View (views.py)
def get_token(request):
    name = request.GET.get("name")
    room = generate_room_name()
    token = AccessToken(API_KEY, API_SECRET)
        .with_identity(name)
        .with_grants(VideoGrants(room_join=True, room=room))
    return JsonResponse({
        'token': token.to_jwt(),
        'room': room,
        'url': LIVEKIT_URL
    })

# 3. Frontend connects to LiveKit with token
<LiveKitRoom token={token} serverUrl={url} />
```

### Agent Processing Flow
```python
# 1. Audio received from user
audio_input → Deepgram STT → text

# 2. Text sent to LLM with context
llm_input = {
    'instructions': TUTOR_PROMPT,
    'user_message': text,
    'conversation_history': history
}

# 3. LLM generates response
response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=llm_input
)

# 4. Response converted to audio
audio_output = openai.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=response.text
)

# 5. Audio sent back to user
audio_output → LiveKit → Browser
```

## Security Architecture

### Token-based Authentication
```
1. User requests session
2. Backend generates JWT token with:
   - Identity (user name)
   - Room permissions
   - Expiration time
3. Token signed with secret key
4. Frontend uses token to connect
5. LiveKit validates token
6. Connection established if valid
```

### Environment Variables Security
```
backend/.env (NOT committed to git)
├── LIVEKIT_API_KEY (Secret)
├── LIVEKIT_API_SECRET (Secret)
├── OPENAI_API_KEY (Secret)
├── DEEPGRAM_API_KEY (Secret)
└── Django settings (Secret)
```

## Scalability Considerations

### Current Architecture
- Single Django server
- Single agent process
- SQLite database
- Suitable for: Development, small deployments

### Production Scaling Options

1. **Backend Scaling**
   - Multiple Django instances with load balancer
   - PostgreSQL instead of SQLite
   - Redis for caching
   - Celery for background tasks

2. **Agent Scaling**
   - Multiple agent processes
   - Agent pool with load balancing
   - Kubernetes deployment
   - Auto-scaling based on demand

3. **LiveKit Scaling**
   - LiveKit Cloud handles this automatically
   - Or self-hosted LiveKit cluster

## Network Requirements

### Ports Used
- `8000` - Django backend (HTTP)
- `5173` - Frontend dev server (HTTP)
- `443/WSS` - LiveKit Cloud (WebSocket Secure)

### Bandwidth
- Audio: ~64 kbps per active session
- Signaling: Minimal
- Transcription data: Minimal

### Latency Targets
- Speech-to-Text: < 500ms
- LLM Processing: < 2000ms
- Text-to-Speech: < 500ms
- Total roundtrip: < 3 seconds

## Database Schema

### Subtopics Table (SQLite)
```sql
CREATE TABLE subtopics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    subtopic TEXT NOT NULL,
    content TEXT NOT NULL
);
```

Used for storing curriculum structure and conversation context.

## Monitoring Points

### What to Monitor
1. **Django Backend**
   - Request latency
   - Error rates
   - Token generation rate

2. **LiveKit Agent**
   - Connection status
   - Processing time
   - Error logs
   - API call counts

3. **External APIs**
   - Deepgram usage/quotas
   - OpenAI usage/costs
   - LiveKit connection status

4. **Frontend**
   - Connection failures
   - Audio quality issues
   - User session duration

## Cost Considerations

### API Costs (Approximate)
- **OpenAI GPT-4**: ~$0.03 per 1K tokens
- **OpenAI TTS**: ~$0.015 per 1K characters
- **Deepgram**: ~$0.0043 per minute
- **LiveKit**: Free tier available, then per-minute pricing

### Cost Optimization
- Use GPT-3.5 instead of GPT-4 if acceptable
- Cache common responses
- Implement session timeouts
- Monitor and set usage limits

---

This architecture provides a solid foundation for voice-based tutoring while remaining extensible for future enhancements.
